try:
    from sage_lib.partition.PartitionManager import PartitionManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PartitionManager: {str(e)}\n")
    del syss

try:
    from sage_lib.IO.structure_handling_tools.AtomPosition import AtomPosition
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing AtomPosition: {str(e)}\n")
    del sys
    
try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys
    
try:
    import numpy as os
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing os: {str(e)}\n")
    del sys
    
try:
    from scipy.optimize import leastsq
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing scipy.optimize.leastsq : {str(e)}\n")
    del sys

class Conductivity_builder(PartitionManager, ):
    """
    Class for building and managing molecular dynamic simulations.
    
    Inherits from PartitionManager and integrates additional functionalities
    specific to molecular dynamics, such as calculating displacement and plotting.

    Attributes:
        _molecule_template (dict): A template for the molecule structure.
        _density (float): Density value of the molecule.
        _cluster_lattice_vectors (numpy.ndarray): Lattice vectors of the cluster.
    """

    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        """
        Initialize the MolecularDynamicBuilder object.

        Args:
            file_location (str, optional): File location of the input data.
            name (str, optional): Name of the simulation.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(name=name, file_location=file_location)

        self._molecule_template = {}
        self._density = None
        self._cluster_lattice_vectors = None


class AtomicDiffusionTools:
    """Collection of functions to help post-processing MD simulations for bulk systems"""

    def __init__(self):
        print("Initializing AtomicDiffusionTools")

    def _isolate_elements(self, atoms, atype):
        """Return a new list of atoms objects only including one selected atom type"""
        print(f"Isolating elements of type: {atype}")
        new_atoms = []
        for i in range(len(atoms)):
            ind = np.where(atoms[i].get_atomic_numbers() == atype)[0]
            new_atoms.append(Atoms(numbers=atoms[i].get_atomic_numbers()[ind],
                                   positions=atoms[i].get_positions()[ind, :], cell=atoms[i].get_cell(),
                                   pbc=True))
        return new_atoms

    def _get_max_displacement(self, atoms):
        """Parse displacements from an atoms trajectory (list), accounting for PBC"""
        print("Calculating maximum displacements")
        pos0, pos_b = atoms[0].get_scaled_positions(), atoms[0].get_scaled_positions()
        dpos_max = np.zeros((pos0[:, 0].size))
        vec_t = np.zeros((pos0[:, 0].size, 3))
        displ = []
        for i in range(len(atoms)):
            pos_c = atoms[i].get_scaled_positions()
            vec_c = self._correct_vec(pos_c - pos_b)
            vec_t += vec_c
            pos_b = pos_c
            vec_tr = np.dot(vec_t, atoms[i].get_cell())
            dpos = np.linalg.norm(vec_tr, axis=1)
            dpos_max = np.transpose(np.vstack((dpos_max, dpos))).max(axis=1)
            displ.append(vec_tr)
        return np.array(displ), dpos_max

    def _correct_vec(self, vec):
        """Correct vectors in fractional coordinates (assuming minimal connection between 2 points)"""
        vec[np.where(vec >= 0.5)] -= 1.0
        vec[np.where(vec < -0.5)] += 1.0
        return vec

    def _calc_current_einstein_time_averaged(self, atoms, charge_dict, lag, atompair=[3, 3], sparsification=10):
        """Calculate the Einstein formulation of the current correlation averaged over a lag time"""
        print("Calculating time-averaged current correlation")
        length = int(len(atoms) * lag)
        inds, qmsd, charges = {'full': range(len(atoms[0]))}, {'full': np.zeros((length, 4))}, atoms[0].get_atomic_numbers()
        charges = np.array([charge_dict[el] for el in charges])
        qd = {'full': np.zeros((length, 4))}
        inds.update({f"{atompair[0]}_{atompair[1]}": np.array(np.where(atoms[0].get_atomic_numbers() == atompair[0])[0].tolist() +
                                                              np.where(atoms[0].get_atomic_numbers() == atompair[1])[0].tolist())})
        qmsd.update({f"{atompair[0]}_{atompair[1]}": np.zeros((length, 4))})
        qd.update({f"{atompair[0]}_{atompair[1]}": np.zeros((length, 4))})
        qmsd_corr = {atompair[0]: np.zeros(length), atompair[1]: np.zeros(length)}
        atypes = np.unique(atoms[0].get_atomic_numbers())
        for atype in atypes:
            qmsd.update({atype: np.zeros((length, 4))})
            qd.update({atype: np.zeros((length, 4))})
            inds.update({atype: np.where(atoms[0].get_atomic_numbers() == atype)[0]})
        sampling_start_list = range(0, len(atoms) + 1 - length, sparsification)

        for i in sampling_start_list:
            print(f"Calculating displacement for sampling start {i}")
            displ, dpos_max = self._get_max_displacement(atoms[i:i + length])
            step_save = {}
            for dtyp in qmsd:
                tqd = self._displ2qd(displ, inds[dtyp], charges)
                qd[dtyp] += tqd / len(inds[dtyp])
                qmsd[dtyp] += tqd**2.0 / len(inds[dtyp])
                step_save.update({dtyp: tqd})
            qmsd_el1_eff, qmsd_el2_eff = self._calc_eff_qmsd(step_save[atompair[0]], step_save[atompair[1]], inds)
            qmsd_corr[atompair[0]] += qmsd_el1_eff
            qmsd_corr[atompair[1]] += qmsd_el2_eff
            print(f"Completed sampling start {i}")
        qmsd.update(qmsd_corr)
        for dtyp in qmsd:
            qmsd[dtyp] /= len(sampling_start_list)
            if dtyp in qd:
                qd[dtyp] /= len(sampling_start_list)
        print("Completed all calculations for QMSD.")
        return qd, qmsd

    def _calc_eff_qmsd(self, qd1, qd2, inds):
        """Calculate effective transport between qd1 and qd2"""
        qmsd1_eff, qmsd2_eff = np.zeros(qd1[:, 0].size), np.zeros(qd2[:, 0].size)
        corr = qd1[:, 0] * qd2[:, 0] + qd1[:, 1] * qd2[:, 1] + qd1[:, 2] * qd2[:, 2]
        qmsd1_eff = (np.linalg.norm(qd1[:, :3], axis=1)**2.0) + corr
        qmsd2_eff = (np.linalg.norm(qd2[:, :3], axis=1)**2.0) + corr
        return qmsd1_eff, qmsd2_eff

    def _displ2qd(self, displ, ind, charges):
        """Calculate Einstein formulation of the current correlation"""
        # Extraemos los desplazamientos específicos una sola vez
        displ_ind = displ[:, ind, :]
        
        # Realizamos operaciones vectorizadas para sumar los productos de cargas y desplazamientos
        q_x = np.sum(charges[ind] * displ_ind[:, :, 0], axis=1)
        q_y = np.sum(charges[ind] * displ_ind[:, :, 1], axis=1)
        q_z = np.sum(charges[ind] * displ_ind[:, :, 2], axis=1)
        
        # Calculamos la magnitud del vector q (q_r) para cada frame
        q_r = np.linalg.norm(np.stack((q_x, q_y, q_z), axis=1), axis=1)
        
        # Combinamos q_x, q_y, q_z y q_r en una sola matriz
        qd = np.stack((q_x, q_y, q_z, q_r), axis=1)
        
        return qd

    def _calc_msd_time_averaged(self, atoms, atypes, lag, sampling_dist=10):
        """Calculate mean square displacement (msd) averaged over a lag time"""
        print("Calculating time-averaged MSD")
        length = int(len(atoms) * lag)
        msd, inds = {}, {}
        for atype in atypes:
            msd.update({atype: np.zeros((length, 4))})
            inds.update({atype: np.where(atoms[0].get_atomic_numbers() == atype)[0]})
        sampling_start_list = range(0, len(atoms) + 1 - length, sampling_dist)
        for i in sampling_start_list:
            displ, dpos_max = self._get_max_displacement(atoms[i:i + length])
            for atype in atypes:
                msd[atype] += self._displ2msd(displ, inds[atype])
            print(f"Completed sampling start {i} for MSD calculation")
        for atype in atypes:
            msd[atype] /= len(sampling_start_list)
        print("Completed all calculations for MSD.")
        return msd

    def _displ2msd(self, displ, ind):
        """Calculate mean squared displacement of dimensions (len(atoms), 4)"""
        msd = []
        for i in range(len(displ)):
            msd_x = np.mean(displ[i][ind, 0] * displ[i][ind, 0])
            msd_y = np.mean(displ[i][ind, 1] * displ[i][ind, 1])
            msd_z = np.mean(displ[i][ind, 2] * displ[i][ind, 2])
            r = np.linalg.norm(displ[i][ind, :], axis=1)
            msd_r = np.mean(r * r)
            msd.append([msd_x, msd_y, msd_z, msd_r])
        return np.array(msd)


def _load_pickle_file(filename):
    """Load data from a pickle file"""
    print(f"Loading pickle file: {filename}")
    with open(filename, 'rb') as pickle_file:
        return pickle.load(pickle_file)


def _write_pickle_file(filename, data):
    """Write data to a pickle file"""
    print(f"Writing data to pickle file: {filename}")
    with open(filename, 'wb') as output:
        pickle.dump(data, output)


def _fit_rates(a, b):
    """Linear regression"""
    fitfunc = lambda p, x: p[0] + p[1] * x
    errfunc = lambda p, x, y: fitfunc(p, x) - y
    p0 = [b[0], (b[-1] - b[0]) / (a.size)]
    pars, success = leastsq(errfunc, p0[:], args=(a, b))
    return pars[1]


def get_diffusion_stats(time, msd):
    """Calculate diffusion coefficients via Einstein relation and anomalous diffusion exponent (alpha)"""
    print("Calculating diffusion stats")
    alpha_exp = _fit_rates(np.log(time[1:] - time[0]), np.log(msd[1:, 3]))
    dfactor = (msd[-1, 3] - msd[0, 3]) / (2 * 3 * (time[-1] - time[0]))
    return dfactor, alpha_exp


def _calc_sigma_from_qmsd(qmsd, time, volume, temp):
    """Calculate sigma from qmsd"""
    print("Calculating sigma from QMSD")
    A2cm, A2m, ps2s = 1e-08, 1e-10, 1e-12
    kB = 1.38064852e-23
    e = 1.60217662e-19
    prefactor = (e * e) / (A2m * A2m * A2m) * ((A2m * A2m) / ps2s)
    sigma = (1 / (time[-1] - time[0])) * (1 / (6 * volume * kB * temp)) * prefactor * (qmsd[-1] - qmsd[0])
    return sigma


def _D2conductivity_nernst(Dm, q, N, volume, temp):
    """Calculate conductivity via Nernst-Einstein relation"""
    print("Calculating conductivity via Nernst-Einstein relation")
    A2cm, A2m, ps2s = 1e-08, 1e-10, 1e-12
    kB = 1.38064852e-23
    e = 1.60217662e-19
    prefactor = (e * e) / (volume * A2m * A2m * A2m * kB * temp) * ((A2m * A2m) / ps2s)
    D_tot = sum([Dm[el] * q[el] * q[el] * N[el] for el in Dm])
    return D_tot * prefactor


def _plot_msd_dict(filename, msd_dict, t, target_folder='output'):
    """Plotting function for msd dictionary"""
    print(f"Plotting MSD dictionary: {filename}")
    colors = ["steelblue", "darkred", "orange"]
    el = np.sort(list(msd_dict.keys()))
    fig, ax1 = plt.subplots()
    mmax = 0
    for i in [0]:
        msd = msd_dict[el[i]]
        mmax = max(mmax, msd[:, 3].max())
        ax1.plot(t[::4], msd[::4, 3], color=colors[i], label=r'%s' % chemical_symbols[el[i]])
        ax1.plot([t[0], t[-1]], [msd[1, 3], msd[1, 3]], color=colors[i], ls=':', lw=1)
        np.savetxt(filename[:-3] + "_li.txt", np.array((t[::4], msd[::4, 3])))
    plt.savefig(f'{target_folder}/{filename}.pdf', bbox_inches='tight')
    fig, ax1 = plt.subplots()
    for i in [1, 2]:
        msd = msd_dict[el[i]]
        mmax = max(mmax, msd[:, 3].max())
        ax1.plot(t[::4], msd[::4, 3], color=colors[i], label=r'%s' % chemical_symbols[el[i]])
        ax1.plot([t[0], t[-1]], [msd[1, 3], msd[1, 3]], color=colors[i], ls=':', lw=1)
        if i == 1:
            np.savetxt(filename[:-3] + "_p.txt", np.array((t[::4], msd[::4, 3])))
        else:
            np.savetxt(filename[:-3] + "_s.txt", np.array((t[::4], msd[::4, 3])))
    ax1.set_xlabel(r'lag time / ps')
    ax1.set_ylabel(r'msd / $\AA^2$')
    plt.legend(prop={"size": 14}, loc="upper left")
    plt.savefig(f'{target_folder}/{filename}_ps.pdf', bbox_inches='tight')


def _plot_msd_all_directions(filename, msd_dict, t):
    """Plot msd in all directions"""
    print(f"Plotting MSD in all directions: {filename}")
    colors = ["steelblue", "darkred", "orange"]
    fig, ax1 = plt.subplots()
    Li_msd = msd_dict.get(3)
    x, y, z = Li_msd[:, 0], Li_msd[:, 1], Li_msd[:, 2]
    ax1.plot(t, x, label='x')
    ax1.plot(t, y, label='y')
    ax1.plot(t, z, label='z')
    plt.legend()
    ax1.set_xlabel(r'lag time / ps')
    ax1.set_ylabel(r'msd / $\AA^2$')
    plt.savefig(f'{filename}.pdf', bbox_inches='tight')
    data = np.concatenate((t, x, y, z))
    np.savetxt(f'{filename}_all.txt', data)


def get_msd(atoms, el_list, sampling_dist=10):
    """Calculate MSD for atoms"""
    print("Calculating MSD for atoms")
    tool = AtomicDiffusionTools()
    msd_dict = tool._calc_msd_time_averaged(atoms, atypes=el_list, lag=1.0, sampling_dist=sampling_dist)
    msd_dict_av = tool._calc_msd_time_averaged(atoms, atypes=el_list, lag=0.7, sampling_dist=sampling_dist)
    return msd_dict, msd_dict_av


def get_msd_conductivity(atoms, temp, el_list=[1, 3, 8, 28], charge_list={1: 1, 3: 1, 8: -2, 28: 1}, outdir="."):
    """Calculate Einstein conductivity"""
    print("Calculating MSD conductivity")
    volume_av = np.average([geom.get_volume() for geom in atoms])
    tool = AtomicDiffusionTools()
    msd_dict = tool._calc_msd_time_averaged(atoms, atypes=el_list, lag=1.0)
    msd_dict_av = tool._calc_msd_time_averaged(atoms, atypes=el_list, lag=0.7)

    for i, dim, color in zip(range(4), ["x", "y", "z", "all"], ["red", "blue", "green", "black"]):
        plt.plot(msd_dict[3][:, i], label=f"msd {dim}", color=color)
        plt.plot(msd_dict_av[3][:, i], color=color, linestyle="dotted")
        np.savetxt(f"{outdir}/msds.txt", msd_dict[3])
        plt.xlabel("t / ps")
        plt.ylabel("msd / $\AA^2$")
        plt.gca().set_aspect((len(msd_dict[3][:, 0])) / (max(msd_dict[3][:, 3]) - min(msd_dict[3][:, 3])), adjustable='box')
        plt.legend()
    plt.tight_layout()
    plt.savefig(f"{outdir}/msd_li.png")
    time = np.arange(msd_dict[list(msd_dict.keys())[0]][:, 0].size)
    time_av = np.arange(msd_dict_av[list(msd_dict_av.keys())[0]][:, 0].size)
    dfactors, dfactors_av = {}, {}
    for el in el_list:
        dfactor, a_exp = get_diffusion_stats(time, msd_dict[el])
        dfactor_av, a_exp_av = get_diffusion_stats(time_av, msd_dict_av[el])
        dfactors.update({el: dfactor})
        dfactors_av.update({el: dfactor_av})
    Nel = {el: np.where(atoms[0].get_atomic_numbers() == el)[0].size for el in el_list}
    sigma = _D2conductivity_nernst(dfactors, q=charge_list, N=Nel, volume=volume_av, temp=temp)
    sigma_av = _D2conductivity_nernst(dfactors_av, q=charge_list, N=Nel, volume=volume_av, temp=temp)
    return sigma, sigma_av


def get_qmsd_conductivity(atoms, temp, sparsification):
    """Calculate full Einstein conductivity including cross terms"""
    print("Calculating QMSD conductivity")
    tool = AtomicDiffusionTools()
    charges = {11: 1, 28: 1, 8: -2, 1: 1}
    qd, qmsd_dict = tool._calc_current_einstein_time_averaged(atoms, charge_dict=charges, lag=1.0, atompair=[11, 1], sparsification=sparsification)
    qd_av, qmsd_dict_av = tool._calc_current_einstein_time_averaged(atoms, charge_dict=charges, lag=0.7, atompair=[11, 1], sparsification=sparsification)
    time = np.arange(qmsd_dict[list(qmsd_dict.keys())[0]][:, 0].size)
    time_av = np.arange(qmsd_dict_av[list(qmsd_dict_av.keys())[0]][:, 0].size)
    sigma = _calc_sigma_from_qmsd(qmsd_dict["11_1"][:, 3], time, volume=atoms[0].get_volume(), temp=temp)
    sigma_av = _calc_sigma_from_qmsd(qmsd_dict_av["11_1"][:, 3], time_av, volume=atoms[0].get_volume(), temp=temp)
    return sigma, sigma_av


def get_haven_ratio(d_tracer, d_current):
    """Calculate Haven ratio"""
    print("Calculating Haven ratio")
    return d_tracer / d_current


def save_conductivity(contents, file="results.txt"):
    """Save conductivity results to file"""
    print(f"Saving conductivity results to file: {file}")
    with open(file, "a") as f:
        f.write(" ".join(str(x) for x in contents) + "\n")


if __name__ == "__main__":
    dir = ""
    msd_sigma, msd_sigma_av, qmsd_sigma, qmsd_sigma_av = [], [], [], []
    for i in range(1):
        print(f"Processing batch {i}")
        atoms = read("diff_500_Li.xyz", "10:")
        data2 = get_msd_conductivity(atoms, temp=500)
        msd_sigma.append(data2[0])
        msd_sigma_av.append(data2[1])
        data_qmsd = get_qmsd_conductivity(atoms, temp=500, sparsification=2)
        qmsd_sigma.append(data_qmsd[0])
        qmsd_sigma_av.append(data_qmsd[1])
    plt.plot(msd_sigma, label="msd_sigma")
    plt.plot(msd_sigma_av, label="msd_sigma_av")
    plt.plot(qmsd_sigma, label="qmsd_sigma")
    plt.plot(qmsd_sigma_av, label="qmsd_sigma_av")
    plt.legend()
    plt.show()

    def _get_max_displacement(self, atoms):
        """Parse displacements from an atoms trajectory (list), accounting for PBC"""
        print("Calculating maximum displacements")
        pos0, pos_b = atoms[0].get_scaled_positions(), atoms[0].get_scaled_positions()
        dpos_max = np.zeros((pos0[:, 0].size))
        vec_t = np.zeros((pos0[:, 0].size, 3))
        displ = []
        for i in range(len(atoms)):
            pos_c = atoms[i].get_scaled_positions()
            vec_c = self._correct_vec(pos_c - pos_b)
            vec_t += vec_c
            pos_b = pos_c
            vec_tr = np.dot(vec_t, atoms[i].get_cell())
            dpos = np.linalg.norm(vec_tr, axis=1)
            dpos_max = np.transpose(np.vstack((dpos_max, dpos))).max(axis=1)
            displ.append(vec_tr)
        return np.array(displ), dpos_max

    def _calc_msd_time_averaged(self, atypes, lag, sampling_dist=10):
        """Calculate mean square displacement (msd) averaged over a lag time"""
        print("Calculating time-averaged MSD")
        length = int(len(atoms) * lag)
        msd, inds = {}, {}
        for atype in atypes:
            msd.update({atype: np.zeros((length, 4))})
            inds.update({atype: np.where(atoms[0].get_atomic_numbers() == atype)[0]})
        sampling_start_list = range(0, len(atoms) + 1 - length, sampling_dist)
        for i in sampling_start_list:
            displ, dpos_max = self._get_max_displacement(atoms[i:i + length])
            for atype in atypes:
                msd[atype] += self._displ2msd(displ, inds[atype])
            print(f"Completed sampling start {i} for MSD calculation")
        for atype in atypes:
            msd[atype] /= len(sampling_start_list)
        print("Completed all calculations for MSD.")
        return msd

    def get_diffusion_stats(self, time, msd):
        """Calculate diffusion coefficients via Einstein relation and anomalous diffusion exponent (alpha)"""
        print("Calculating diffusion stats")
        alpha_exp = _fit_rates(np.log(time[1:] - time[0]), np.log(msd[1:, 3]))
        dfactor = (msd[-1, 3] - msd[0, 3]) / (2 * 3 * (time[-1] - time[0]))
        return dfactor, alpha_exp

    def get_msd_conductivity(T, atom_types:list=None, charge_list={1: 1, 3: 1, 8: -2, 28: 1}, verbosity:bool=False):
        """Calculate Einstein conductivity"""
        if verbosity: print("Calculating MSD conductivity")
        
        volume_av = np.average([container.AtomPositionManager.get_volume() for container in self.containers])

        atom_types = list(set([container.AtomPositionManager.uniqueAtomLabels for container in self.containers ])) if atom_types is None else atom_types

        msd_dict = self._calc_msd_time_averaged(atypes=atom_types, lag=1.0)
        msd_dict_av = self._calc_msd_time_averaged(atypes=atom_types, lag=0.7)

        time = np.arange(msd_dict[list(msd_dict.keys())[0]][:, 0].size)
        time_av = np.arange(msd_dict_av[list(msd_dict_av.keys())[0]][:, 0].size)
        
        dfactors, dfactors_av = {}, {}

        for el in atom_types:
            dfactor, a_exp = self.get_diffusion_stats(time, msd_dict[el])
            dfactor_av, a_exp_av = self.get_diffusion_stats(time_av, msd_dict_av[el])
            dfactors.update({el: dfactor})
            dfactors_av.update({el: dfactor_av})


        tool = AtomicDiffusionTools()
        msd_dict = tool._calc_msd_time_averaged(atoms, atypes=el_list, lag=1.0)
        msd_dict_av = tool._calc_msd_time_averaged(atoms, atypes=el_list, lag=0.7)

        for i, dim, color in zip(range(4), ["x", "y", "z", "all"], ["red", "blue", "green", "black"]):
            plt.plot(msd_dict[3][:, i], label=f"msd {dim}", color=color)
            plt.plot(msd_dict_av[3][:, i], color=color, linestyle="dotted")
            np.savetxt(f"{outdir}/msds.txt", msd_dict[3])
            plt.xlabel("t / ps")
            plt.ylabel("msd / $\AA^2$")
            plt.gca().set_aspect((len(msd_dict[3][:, 0])) / (max(msd_dict[3][:, 3]) - min(msd_dict[3][:, 3])), adjustable='box')
            plt.legend()
        plt.tight_layout()
        plt.savefig(f"{outdir}/msd_li.png")
        time = np.arange(msd_dict[list(msd_dict.keys())[0]][:, 0].size)
        time_av = np.arange(msd_dict_av[list(msd_dict_av.keys())[0]][:, 0].size)
        dfactors, dfactors_av = {}, {}

        for el in el_list:
            dfactor, a_exp = get_diffusion_stats(time, msd_dict[el])
            dfactor_av, a_exp_av = get_diffusion_stats(time_av, msd_dict_av[el])
            dfactors.update({el: dfactor})
            dfactors_av.update({el: dfactor_av})
        Nel = {el: np.where(atoms[0].get_atomic_numbers() == el)[0].size for el in el_list}
        sigma = _D2conductivity_nernst(dfactors, q=charge_list, N=Nel, volume=volume_av, temp=temp)
        sigma_av = _D2conductivity_nernst(dfactors_av, q=charge_list, N=Nel, volume=volume_av, temp=temp)
        return sigma, sigma_av


    def handle_conductivity_analysis(self, values:list ):

        conductivity_data = {}

        for v in values:

            if plot.upper() == 'diffusion':    
                msd_sigma,msd_sigma_av  = self.get_msd_conductivity( T=values[plot].get('T', False) )
                qmsd_sigma, qmsd_sigma_av = self.get_qmsd_conductivity( T=values[plot].get('T', False), sparsification=values[plot].get('sparsification', 1))
















