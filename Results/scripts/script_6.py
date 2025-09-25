# Save the test results to Excel file in the correct format
print("Saving results to Excel file...")

# Save to Excel file matching the output structure
output_filename = "Text_Analysis_Results.xlsx"
results_df.to_excel(output_filename, index=False)
print(f"Results saved to {output_filename}")

# Display summary statistics
print("\n=== SUMMARY STATISTICS ===")
print(f"Total articles processed: {len(results_df)}")
print(f"Articles with content extracted: {sum(1 for _, row in results_df.iterrows() if row['WORD COUNT'] > 0)}")

print("\nAverage metrics across all articles:")
numeric_columns = [col for col in results_df.columns if col not in ['URL_ID', 'URL']]
for col in numeric_columns:
    avg_val = results_df[col].mean()
    print(f"  {col}: {avg_val:.4f}")

print("\nRange of values:")
for col in numeric_columns:
    min_val = results_df[col].min()
    max_val = results_df[col].max()
    print(f"  {col}: {min_val:.4f} - {max_val:.4f}")

# Display the complete results table
print("\n=== COMPLETE RESULTS TABLE ===")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)
print(results_df.to_string(index=False))