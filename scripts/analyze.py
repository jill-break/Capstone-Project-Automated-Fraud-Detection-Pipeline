import sys
import csv
import datetime

def analyze_fraud():
    # Read input from the pipe (stdin)
    input_data = sys.stdin.read().strip()
    
    if not input_data:
        print("No data received.")
        return

    # Parse the CSV data
    lines = input_data.split('\n')
    reader = csv.DictReader(lines)
    
    # Define the output file name
    output_file = "fraud reports/fraud_report.txt"
    
    with open(output_file, "w") as f:
        # Write Header with Timestamp
        f.write(f"--- AI FRAUD ANALYSIS REPORT ---\n")
        f.write(f"Generated on: {datetime.datetime.now()}\n")
        f.write("-" * 40 + "\n\n")
        
        anomalies_found = 0

        for row in reader:
            user = row.get('user_id')
            amount = float(row.get('amount', 0))
            z_score = float(row.get('z_score', 0))
            category = row.get('merchant_category')

            # Logic: Check for Z-Score > 2
            if z_score > 2:
                anomalies_found += 1
                explanation = (
                    f"CRITICAL ALERT: User {user} initiated a high-value transaction of ${amount:,.2f} "
                    f"in the '{category}' category.\n"
                    f"   -> Statistical Insight: The Z-Score is {z_score:.2f}, indicating this deviation "
                    f"is significantly rare (top 2% of variance).\n"
                    f"   -> Recommended Action: Immediate Freeze.\n"
                )
                f.write(explanation + "\n")
                # OPTIONAL: Still print critical alerts to console for immediate visibility
                print(f"  ALERT GENERATED: User {user} | Z-Score: {z_score:.2f}")
            else:
                f.write(f"User {user}: Transaction appears normal.\n")

        # Footer
        f.write(f"\n--- End of Report ---\n")
        f.write(f"Total Anomalies Detected: {anomalies_found}")

    print(f"\n Analysis complete. Full report saved to '{output_file}'.")

if __name__ == "__main__":
    analyze_fraud()