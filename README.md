📊 Customer Sales Analyser

A web-based data analysis tool built with Streamlit that accepts any CSV file 
and generates instant statistical insights.

🚀 Features

Descriptive Statistics — Mean, Median, Mode, Variance, Std Dev, Skewness
Distribution Analysis — Identifies normal, right-skewed, or left-skewed distributions
Outlier Detection — Flags values beyond Mean ± 2 SD
Histogram — Visual distribution with Mean, Median and SD boundary lines
Correlation Analysis — Pearson r between any two numeric columns with scatter plot
Random Sampling — Compare sample vs population mean with adjustable sample size

🛠️ Built With

- Python 3.14
- Streamlit
- pandas
- NumPy
- SciPy
- matplotlib
⚙️ How to Run

1. Clone the repo: git clone https://github.com/dilliganesh5/customer-sales-analyser.git

2. Install dependencies:

pip install streamlit pandas numpy scipy matplotlib

3. Run the app:

streamlit run sales_analyser.py

4. Upload any CSV file with numeric columns and explore the insights.

📁 Expected Input Format

Any `.csv` file with at least one numeric column.

Example:

Name,Purchases,Age
Alice,1200,25
Bob,3400,32
Carol,850,28
