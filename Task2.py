import pandas as pd
from fpdf import FPDF
from datetime import date

# ----------------------------
# READ AND ANALYZE DATA
# ----------------------------
def read_and_analyze(file_path):
    df = pd.read_csv(file_path)
    avg_score = df['Score'].mean()
    top_performer = df.loc[df['Score'].idxmax()]
    dept_summary = df.groupby('Department')['Score'].mean().reset_index()
    return avg_score, top_performer, dept_summary, df

# ----------------------------
# GENERATE PDF REPORT
# ----------------------------
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Intern Performance Report", ln=True, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Generated on {date.today()}", align="C")

    def add_content(self, avg_score, top_performer, dept_summary, df):
        self.set_font("Arial", "", 12)
        self.ln(10)
        self.cell(0, 10, f"Average Score: {avg_score:.2f}", ln=True)
        self.cell(0, 10, f"Top Performer: {top_performer['Name']} with score {top_performer['Score']}", ln=True)

        self.ln(10)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Average Score by Department:", ln=True)
        self.set_font("Arial", "", 12)
        for _, row in dept_summary.iterrows():
            self.cell(0, 10, f"{row['Department']}: {row['Score']:.2f}", ln=True)

        self.ln(10)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Individual Scores:", ln=True)
        self.set_font("Arial", "", 12)
        for _, row in df.iterrows():
            self.cell(0, 10, f"{row['Name']} - {row['Department']} - {row['Score']}", ln=True)

# ----------------------------
# MAIN EXECUTION
# ----------------------------
def main():
    file_path = 'sample_data.csv'
    avg_score, top_performer, dept_summary, df = read_and_analyze(file_path)

    pdf = PDFReport()
    pdf.add_page()
    pdf.add_content(avg_score, top_performer, dept_summary, df)
    pdf.output("Intern_Report.pdf")

    print("PDF Report generated: Intern_Report.pdf")

if __name__ == "__main__":
    main()
