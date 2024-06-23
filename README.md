# Soil Moisture Model in Python
Soil water balance model for estimating soil moisture

The model can be freely applied and used, just cite some of the references to the model reported below.
The authors are highly interested to collaborate for the understanding of the model functioning and to improve its performance and applicability.

For any questions please do not hesitate to contact:
luca.brocca@irpi.cnr.it
(code converted in Python from Hamidreza Mosaffa)

-------------------------------------------

"SM_Model_IE.py": Soil Moisture Model

"data.txt": Data for the example (date, precipitation [mm], air temperature [°C] and relative soil moisture [% saturation])

"Figure.png": Figure with the model results

"Xopt.txt": Optimal set of parameter values for the selected data in the example

(a Matlab version is also available: https://github.com/lucabrocca78/Soil-Moisture-Model-Matlab)

-------------------------------------------

# Main References
Brocca, L., Melone, F., Moramarco, T. (2008). On the estimation of antecedent wetness conditions in rainfall-runoff modelling. Hydrological Processes, 22 (5), 629-642, doi:10.1002/hyp.6629. http://dx.doi.org/10.1002/hyp.6629

Brocca, L., Camici, S., Melone, F., Moramarco, T., Martinez-Fernandez, J., Didon-Lescot, J.-F., Morbidelli, R. (2014). Improving the representation of soil moisture by using a semi-analytical infiltration model. Hydrological Processes, 28(4), 2103-2115, doi:10.1002/hyp.9766. http://dx.doi.org/10.1002/hyp.9766

------
# python code: 

Requirements
Ensure you have the following Python packages installed:
•	numpy
•	pandas
•	matplotlib
•	datetime

You can install them using pip if not already installed:
pip install numpy pandas matplotlib

# Running the Code
1.	Place the files: Ensure SM_Model_IE.py, data.txt, Xopt.txt, and the folder where you want Figure.png to be saved are in the same directory.
2.	Edit the paths: In SM_Model_IE.py, update the file paths for data.txt, Xopt.txt, and the output path for Figure.png to match your directory structure. For

example:
PTSM = np.loadtxt("path/to/data.txt")
PAR = np.loadtxt("path/to/Xopt.txt")
namefig = 'path/to/figure.png'

3.	Run the script: Execute the script from your terminal or command prompt:
python SM_Model_IE.py
4.	Output: After running the script, Figure.png will be generated in the specified directory. This file contains the graphical results of the soil moisture model.

# Code Overview
Functions
1.	matlab2PythonDates(dateMatlab):
o	Converts MATLAB date numbers to Python datetime objects.
2.	kling_gupta_efficiency(sim, obs):
o	Calculates the Kling-Gupta Efficiency (KGE) between simulated and observed data.
3.	SMestim_IE_02(PTSM, PAR, FIG, namefig):
o	Main function to estimate soil moisture.
o	Inputs:
	PTSM: Array of input data (dates, precipitation, temperature, soil moisture).
	PAR: Array of model parameters.
	FIG: Indicator for plotting results.
	namefig: Path for saving the output figure.
o	Outputs:
	WW: Simulated soil moisture.
	NS: Nash-Sutcliffe efficiency.
	KGE: Kling-Gupta Efficiency.
5.	plot_results(D, WW, WWobs, PIO, NS, NS_lnQ, NS_radQ, RQ, RMSE, KGE, namefig): Plots and saves the model results.

