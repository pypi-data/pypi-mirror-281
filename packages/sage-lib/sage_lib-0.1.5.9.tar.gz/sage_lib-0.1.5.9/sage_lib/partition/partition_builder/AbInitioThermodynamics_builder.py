try:
    from sage_lib.partition.PartitionManager import PartitionManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing PartitionManager: {str(e)}\n")
    del syss

try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

try:
    from sklearn.manifold import TSNE
    from scipy.spatial import cKDTree
    from sklearn.decomposition import PCA
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing sklearn.manifold: {str(e)}\n")
    del sys

try:
    import copy
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing copy: {str(e)}\n")
    del sys

try:
    import os
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing os: {str(e)}\n")
    del sys
    
try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing matplotlib.pyplot: {str(e)}\n")
    del sys
    
try:
    import seaborn as sns
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while seaborn: {str(e)}\n")
    del sys


class AbInitioThermodynamics_builder(PartitionManager):
    """

    """

    def __init__(self, file_location:str=None, name:str=None, **kwargs):
        """

        """
        super().__init__(name=name, file_location=file_location)
        
        self.composition_data = None
        self.energy_data = None 
        self.area_data = None

    def get_composition_data(self, ) -> dict:
        # 
        composition_data, energy_data, area_data = np.zeros((len(self.containers), len(self.uniqueAtomLabels)), dtype=np.float64), np.zeros(len(self.containers), dtype=np.float64), np.zeros(len(self.containers), dtype=np.float64)
        for c_i, c in enumerate(self.containers):  
            comp = np.zeros_like( self.uniqueAtomLabels, dtype=np.int64 )
            for ual, ac in zip(c.AtomPositionManager.uniqueAtomLabels, c.AtomPositionManager.atomCountByType):
                comp[ self.uniqueAtomLabels_order[ual] ] = ac 

            composition_data[c_i,:] = comp
            energy_data[c_i] = c.AtomPositionManager.E
            area_data[c_i] = c.AtomPositionManager.get_area('z')

        self.composition_data, self.energy_data, self.area_data = composition_data, energy_data, area_data

        return {'composition_data': composition_data, 'energy_data':energy_data, 'area_data':area_data}


    def get_diagram_data(self, ID_reference:list, composition_data:np.array, energy_data:np.array, area_data:np.array, especie:str) -> np.array:
        composition_reference = composition_data[ID_reference, :] 
        energy_reference = energy_data[ID_reference] 
        self.uniqueAtomLabels_order

        for cr_i, cr in enumerate(composition_reference): 
            if np.sum(cr) == cr[ self.uniqueAtomLabels_order[especie] ]:
                reference_mu_index = cr_i

        mask = np.ones(len(energy_data), dtype=bool)
        mask[ID_reference] = False

        composition_relevant = composition_data[mask,:]
        energy_relevant = energy_data[mask]
        area_relevant = area_data[mask]

        diagram_data = np.zeros( (energy_relevant.shape[0], 2) )

        for mu in [0, 1]:
            for i, (E, C, A) in enumerate(zip(energy_relevant, composition_relevant, area_relevant)):
                E_ref_mask = np.zeros_like(energy_reference)
                E_ref_mask[reference_mu_index] = mu

                mu_value = np.linalg.solve(composition_reference, energy_reference+E_ref_mask)
                gamma = 1/A * E * np.sum( mu_value * C ) 

                diagram_data[i, mu] = gamma

        return diagram_data


    def get_diagram_data(self, ID_reference:list, composition_data:np.array, energy_data:np.array, area_data:np.array, especie:str) -> np.array:
        composition_reference = composition_data[ID_reference, :] 
        energy_reference = energy_data[ID_reference] 
        self.uniqueAtomLabels_order

        for cr_i, cr in enumerate(composition_reference): 
            if np.sum(cr) == cr[ self.uniqueAtomLabels_order[especie] ]:
                reference_mu_index = cr_i

        mask = np.ones(len(energy_data), dtype=bool)
        mask[ID_reference] = False

        composition_relevant = composition_data[mask,:]
        energy_relevant = energy_data[mask]
        area_relevant = area_data[mask]

        diagram_data = np.zeros( (energy_relevant.shape[0], 2) )

        for mu in [0, 1]:
            for i, (E, C, A) in enumerate(zip(energy_relevant, composition_relevant, area_relevant)):
                E_ref_mask = np.zeros_like(energy_reference)
                E_ref_mask[reference_mu_index] = mu

                mu_value = np.linalg.solve(composition_reference, energy_reference+E_ref_mask)
                gamma = 1/A * E * np.sum( mu_value * C ) 

                diagram_data[i, mu] = gamma

        return diagram_data

    def global_linear_predict(self, compositions, energies, regularization=1e-8, verbose:bool=False, center:bool=True):
        """
        """

        # Center the compositions by subtracting the target composition
        mean_compositions = np.mean(compositions) if center else 0
        centered_compositions = compositions - mean_compositions 

        weights = np.ones_like(energies)

        # Normalize the weights
        weights /= weights.sum()  

        # Solve the linear system to find the coefficients with regularization
        A = np.dot(centered_compositions.T, centered_compositions * weights[:, np.newaxis])
        A += regularization * np.eye(A.shape[0])  # Add regularization term to the diagonal
        
        # Center the energies
        mean_energy = np.mean(energies) if center else 0
        centered_energies = energies - mean_energy

        B = np.dot(centered_compositions.T, centered_energies * weights)
        coeffs = np.linalg.solve(A, B)

        print(coeffs.shape, centered_compositions.shape)
        # Predict the energy using the linear combination of the neighbors
        predicted_energy = mean_energy + np.dot(coeffs, centered_compositions.T )

        if verbose: 
            print(f"Centered compositions: \n{centered_compositions}")
            print(f"Coefficients: \n{coeffs}")
            print(f"Predicted energy: {predicted_energy}")
                 
        return compositions, predicted_energy, coeffs

    def locally_linear_predict(self, compositions, energies, target, k=5, regularization=1e-8, verbose:bool=False, center:bool=True, weights:str='none'):
        """
        Predict the energy for a target composition using locally linear regression with regularization.
        
        Parameters:
        compositions (np.ndarray): Array of shape (n_samples, 5) containing the composition points.
        energies (np.ndarray): Array of shape (n_samples,) containing the energy values for each composition point.
        target (np.ndarray): Array of shape (5,) representing the target composition for which to predict the energy.
        k (int): Number of nearest neighbors to use for the prediction.
        regularization (float): Regularization parameter to avoid singular matrix errors (default is 1e-5).
        
        Returns:
        float: Predicted energy for the target composition.
        """

        # Build a KD-tree for efficient neighbor search
        tree = cKDTree(compositions)
        
        # Find the k nearest neighbors to the target point
        distances, indices = tree.query(target, k=k)

        # Get the nearest neighbor compositions and their corresponding energies
        nearest_compositions = compositions[indices]
        nearest_energies = energies[indices]
        
        # Center the compositions by subtracting the target composition
        mean_target = np.mean(target) if center else 0
        centered_compositions = nearest_compositions - mean_target 

        if weights == 'distances':
            # Compute the weights inversely proportional to the distances
            weights = np.exp(-distances) # np.ones_like(distances) # np.exp(-distances)
        else:
            # no weights
            weights = np.ones_like(distances)

        # Normalize the weights
        weights /= weights.sum()  

        # Solve the linear system to find the coefficients with regularization
        A = np.dot(centered_compositions.T, centered_compositions * weights[:, np.newaxis])
        A += regularization * np.eye(A.shape[0])  # Add regularization term to the diagonal
        
        # Center the energies
        mean_energy = np.mean(nearest_energies) if center else 0
        centered_energies = nearest_energies - mean_energy

        B = np.dot(centered_compositions.T, centered_energies * weights)
        coeffs = np.linalg.solve(A, B)

        # Predict the energy using the linear combination of the neighbors
        predicted_energy = mean_energy + np.dot(coeffs, target - mean_target )

        if verbose: 
            print(f"Nearest compositions: \n{nearest_compositions}")
            print(f"Target composition: \n{target}")
            print(f"Distances: \n{distances}")
            print(f"Weights: \n{weights}")
            print(f"Centered compositions: \n{centered_compositions}")
            print(f"Coefficients: \n{coeffs}")
            print(f"Predicted energy: {predicted_energy}")
                 
        return predicted_energy, coeffs

    def n_fold_cross_validation(self, compositions, energies, k=20, output_path:str=None, verbose:bool=False):
        """
        Perform N-fold cross-validation to estimate prediction errors for each composition.
        
        Parameters:
        compositions (np.ndarray): Array of shape (n_samples, 5) containing the composition points.
        energies (np.ndarray): Array of shape (n_samples,) containing the energy values for each composition point.
        k (int): Number of nearest neighbors to use for the prediction.
        
        Returns:
        list: List of tuples containing (composition, prediction error) for each test point.
        """
        unique_compositions = np.unique(compositions, axis=0)
        errors = []
        predicted_E = []
        composition_data = []
        coeffs_data = []

        for i, comp in enumerate(unique_compositions):
            if verbose:
                print(f" >> ({i}) Unique composition: {comp} ")
            # Separar los datos de entrenamiento y prueba
            mask = np.all(compositions == comp, axis=1)
            train_compositions = compositions[~mask]
            train_energies = energies[~mask]
            test_compositions = compositions[mask]
            test_energies = energies[mask]

            # Predecir las energías para las composiciones de prueba
            for test_comp, real_energy in zip(test_compositions, test_energies):
                if verbose:
                    print(f" >> >> Test composition {test_comp} :: E = {real_energy}")
                predicted_energy, coeffs = self.locally_linear_predict(train_compositions, train_energies, test_comp, k, verbose=verbose)
                error = predicted_energy - real_energy #np.abs(predicted_energy - real_energy)

                coeffs_data.append( coeffs )
                errors.append( error/np.sum(test_comp) )
                predicted_E.append(predicted_energy)
                composition_data.append( test_comp )

        data = np.array([ np.append(c, e) for e, c in zip(errors, composition_data) ])

        self.save_array_to_csv(data, column_names=np.append(self.uniqueAtomLabels,'e'), sample_numbers=True, file_path='.')

        return np.array(errors), np.array(predicted_E), np.array(composition_data), np.array(coeffs_data)

    def find_optimal_k(self, composition_data: dict = None, initial_step: int = 10, refinement_step: int = 1, verbose: bool = False):
        """
        Find the optimal value of k for locally linear regression using a two-step approach.
        
        Parameters:
        composition_data (dict): Dictionary containing 'composition_data' (np.ndarray) and 'energy_data' (np.ndarray).
        initial_step (int): Step size for the initial broad search of k values.
        refinement_step (int): Step size for the refined search within regions of interest.
        verbose (bool): If True, prints detailed information and progress.
        
        Returns:
        tuple: Optimal value of k, errors, and predicted energies.
        """
        if composition_data is None:
            raise ValueError("composition_data cannot be None")

        compositions = composition_data['composition_data']
        energies = composition_data['energy_data']
        n_samples = int(compositions.shape[0]*.9)

        # Initial broad search
        k_values = range(compositions[0].shape[0]-1, n_samples, initial_step)
        initial_errors = []
        error_history = []
        coeffs_history = []

        for idx, k in enumerate(k_values):
            errors, predicted_E, _, coeffs = self.n_fold_cross_validation(compositions=compositions, energies=energies, k=k, verbose=False)
            current_rmse = np.mean(errors**2)**0.5
            initial_errors.append((k, current_rmse))
            error_history.append(current_rmse)
            coeffs_history.append(coeffs)

            if verbose:
                print(f"Initial search - k: {k}, RMSE: {initial_errors[-1][1]:.4f}, Progress: {100*(idx+1)/len(k_values):.2f}%")

            # Early stopping condition
            if len(error_history) > 4 and all(abs(error_history[-i-1] - error_history[-i-2]) < 1e-4 for i in range(1, 5)):
                if verbose:
                    print(f"Early stopping at k: {k} due to minimal change in error.")
                break

        # Find the best k in the initial search
        initial_best_k = min(initial_errors, key=lambda x: x[1])[0]
        if verbose:
            print(f"Best k after initial search: {initial_best_k}")

        # Refine search around the best k
        refined_range = range(max(1, initial_best_k - initial_step), min(n_samples, initial_best_k + initial_step), refinement_step)
        refined_errors = []
        for idx, k in enumerate(refined_range):
            errors, predicted_E, _, coeffs = self.n_fold_cross_validation(compositions=compositions, energies=energies, k=k, verbose=False)
            current_rmse = np.mean(errors**2)**0.5
            refined_errors.append((k, current_rmse))
            coeffs_history.append(coeffs)

            if verbose:
                print(f"Refined search - k: {k}, RMSE: {refined_errors[-1][1]:.4f}, Progress: {100*(idx+1)/len(refined_range):.2f}%")

        # Find the best k in the refined search
        best_k = min(refined_errors, key=lambda x: x[1])[0]
        if verbose:
            print(f"Optimal k after refined search: {best_k}")

        # Return the best k and associated errors
        return best_k, initial_errors, refined_errors, np.array(coeffs_history)

    def plot_k_convergence(self, initial_errors, refined_errors, coeffs, output_path=None, verbose=False):
        """
        Plot the convergence of the error with respect to different k values.
        
        Parameters:
        initial_errors (list): List of tuples (k, RMSE) from the initial broad search.
        refined_errors (list): List of tuples (k, RMSE) from the refined search.
        output_path (str): Path to save the plot. If None, the plot is displayed.
        verbose (bool): If True, prints additional information.
        """

        # Extract k values and errors
        initial_k, initial_rmse = zip(*initial_errors)
        refined_k, refined_rmse = zip(*refined_errors)
        
        # Create the plot
        fig, ax = plt.subplots(2, 1, figsize=(10, 12))

        # Plot RMSE convergence
        ax[0].plot(initial_k, initial_rmse, 'o-', label='Initial Search', color='blue')
        ax[0].plot(refined_k, refined_rmse, 'x-', label='Refined Search', color='red')
        ax[0].set_xlabel('k value')
        ax[0].set_ylabel('RMSE')
        ax[0].set_title('Convergence of RMSE with Different k Values')
        ax[0].legend()
        ax[0].grid(True)
        
        # Plot coefficients as a scatter plot with lines
        N, samples, atom_types = coeffs.shape
        colors = plt.cm.viridis(np.linspace(0, 1, atom_types))
        
        for atom_type in range(atom_types):
            for n in range(samples):
                if n == 0:
                    ax[1].plot( initial_k+refined_k, coeffs[:, n, atom_type], 'o-', color=colors[atom_type], alpha=0.2, label=f'{self.uniqueAtomLabels[atom_type]}')
                else:
                    ax[1].plot( initial_k+refined_k, coeffs[:, n, atom_type], 'o-', color=colors[atom_type], alpha=0.2)

        ax[1].set_xlabel('k value')
        ax[1].set_ylabel('Coefficient Value')
        ax[1].set_title('Coefficients Scatter Plot')
        ax[1].legend()

        # Adjust layout and save or show the plot
        plt.tight_layout()
        
        # Save or display the plot
        if output_path:
            plt.savefig(output_path + '/k_convergence_with_coeffs.png', dpi=300)
            if verbose:
                print(f"Convergence plot with coefficients saved to {output_path + '/k_convergence_with_coeffs.png'}")
        else:
            plt.show()

    def plot_phase_diagram(self, diagram_data:np.array, mu_max:float, mu_min:float, output_path:str=None, window_size:tuple=(10, 6), save:bool=True, verbose:bool=True):
        """
        Plot a phase diagram with extrapolated lines from given points and highlight the lower envelope.

        Parameters:
        - diagram_data (np.ndarray): An Nx2 array with each row being [y-intercept, slope] for a line.
        - output_path (str, optional): Path to save the plot image.
        - window_size (tuple, optional): Size of the plotting window.
        - save (bool, optional): Whether to save the plot to a file.
        - verbose (bool, optional): Whether to print additional information.
        """
        # Define plot limits
        pd_min, pd_max = mu_min, mu_max  # Adjust as needed

        plt.figure(figsize=window_size)

        # For each line, calculate and plot
        for index, (x, y) in enumerate(diagram_data):
            # Calculate slope (m) and y-intercept (b) for the line
            m = (y - x) / (1 - 0)  # (y2-y1)/(x2-x1)
            b = y - m * 1  # y = mx + b => b = y - mx
            
            # Generate x values from pd_min to pd_max for plotting
            x_values = np.linspace(pd_min, pd_max, 100)
            # Calculate y values based on the line equation
            y_values = m * x_values + b
            
            # Plot each line
            plt.plot(x_values, y_values, alpha=0.5, label=f'Line {index}')

        opt_estructures = []
        # TODO: Identify and plot the lower envelope
        # This requires a custom implementation based on your criteria for the lower envelope.
        
        # Customize the plot
        plt.legend()
        plt.xlabel('X Axis')
        plt.ylabel('Y Axis')
        plt.title('Phase Diagram with Lower Envelope Highlighted')

        # Show or save the plot
        if save:
            if not output_path:
                output_path = '.'  # Use current directory if not specified
            plt.savefig(f'{output_path}/phase_diagram_plot.png', dpi=100)
        else:
            plt.show()

    def plot_manifold(self, features:np.array, response:np.array, output_path:str=None, save:bool=True, verbose:bool=True) -> bool:
        # Using T-SNE to reduce to 2 dimensions
        tsne = TSNE(n_components=2, random_state=42)
        tsne_results = tsne.fit_transform(features)

        # Using PCA to reduce to 2 dimensions (for visualization purposes)
        pca = PCA(n_components=3)  # Specify 3 components for 3D plot
        pca_results = pca.fit_transform(features)
        explained_variance = pca.explained_variance_ratio_

        # Create plots of the results
        fig, ax = plt.subplots(1, 3, figsize=(18, 6))

        # T-SNE plot
        sc = ax[0].scatter(tsne_results[:, 0], tsne_results[:, 1], c=response, cmap='viridis')
        ax[0].set_title('T-SNE Results')
        ax[0].set_xlabel('T-SNE Component 1')
        ax[0].set_ylabel('T-SNE Component 2')
        plt.colorbar(sc, ax=ax[0], label='Energy')

        # PCA plot (2D projection)
        sc_pca = ax[1].scatter(pca_results[:, 0], pca_results[:, 1], c=response, cmap='viridis')
        ax[1].set_title('PCA Results (2D projection)')
        ax[1].set_xlabel(f'PCA Component 1 ({explained_variance[0]*100:.2f}% variance)')
        ax[1].set_ylabel(f'PCA Component 2 ({explained_variance[1]*100:.2f}% variance)')
        plt.colorbar(sc_pca, ax=ax[1], label='Energy')

        # Response plot
        ax[2].plot(response, 'o-', c=(0.8, 0.3, 0.3))
        RMSE = np.mean( (response)**2 )**0.5
        ax[2].plot([0, response.shape[0]], [RMSE, RMSE], '-', c=(0.8, 0.8, 0.3), alpha=0.6, label=f'RMSE:{RMSE:.5f}')
        ax[2].set_title('Response Plot')
        ax[2].set_xlabel('Index')
        ax[2].set_ylabel('Response (Energy)')
        ax[2].legend()

        # Adjust layout and save or show the plot
        plt.tight_layout()

        # Show or save the plot
        if save:
            if not output_path:
                output_path = '.'  # Use current directory if not specified
            plt.savefig(f'{output_path}/manifold_plot.png', dpi=100)

        else:
            plt.show()

        if verbose:
            print(f"PCA explained variance ratios: {explained_variance}")
            print(f"Saved plot to {output_path}/manifold_plot.png")


    def handleABITAnalysis(self, values:list, file_location:str=None):
        """
        Handle molecular dynamics analysis based on specified values.

        Args:
            values (list): List of analysis types to perform.
            file_location (str, optional): File location for output data.
        """
        ABIT_data = {}

        for abit in values:
            if abit.upper() == 'PHASE_DIAGRAM':
                composition_data = self.get_composition_data()
                diagram_data = self.get_diagram_data(ID_reference=values[abit].get('reference_ID', [0]), 
                                    composition_data=composition_data['composition_data'], energy_data=composition_data['energy_data'], area_data=composition_data['area_data'], 
                                     especie=values[abit].get('especie', None)) 
                self.plot_phase_diagram(diagram_data, output_path=values[abit].get('output_path', '.'), save=True, verbose=values[abit].get('verbose', True), mu_max=values[abit].get('mu_max', [0]), mu_min=values[abit].get('mu_min', [0]))

            if abit.upper() == 'LOCAL_LINEAR':
                composition_data = self.get_composition_data()

                if values[abit].get('opt', True):
                    values[abit]['k'], initial_errors, refined_errors, coeffs = self.find_optimal_k(composition_data=composition_data, verbose=values[abit].get('verbose', False))
                    self.plot_k_convergence(initial_errors, refined_errors, coeffs=coeffs, output_path=values[abit].get('output_path', '.'))

                errors, predicted_E, composition_data, coeffs = self.n_fold_cross_validation(compositions=composition_data['composition_data'], energies=composition_data['energy_data'], k=values[abit]['k'], output_path=values[abit].get('output_path', '.'), verbose=values[abit].get('verbose', False)) 
                
                if values[abit].get('output_path', False):
                    self.plot_manifold(features=composition_data, response=errors, output_path=values[abit].get('output_path', '.'), save=True, verbose=values[abit].get('verbose', True), ) 

            if abit.upper() == 'GLOBAL_LINEAR':
                composition_data = self.get_composition_data()
                composition, predicted_E, coeffs = self.global_linear_predict(compositions=composition_data['composition_data'], energies=composition_data['energy_data'], regularization=1e-8, verbose=values[abit].get('verbose', True), center=True)
                print(composition)
                asd
                if values[abit].get('output_path', False):
                    self.plot_manifold(features=composition, response=composition_data['energy_data']-predicted_E, output_path=values[abit].get('output_path', '.'), save=True, verbose=values[abit].get('verbose', True), ) 


