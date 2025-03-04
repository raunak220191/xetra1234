1.	Reference Table
Use the following table as a guide for Final Level values (from 0.0 to 2.0). Columns I, II, and III are indicative of different scenarios or underliers; the Payoff column will be computed based on the conditions below:
| FINAL LEVEL |    I    |    II   |   III   | Payoff (To be computed) |
|-------------|---------|---------|---------|-------------------------|
| 0.1         | 0.0000  | 0.0000  | 0.0000  |                         |
| 0.2         | 0.1000  | 0.1000  | 0.1000  |                         |
| 0.3         | 0.2000  | 0.2000  | 0.2000  |                         |
| 0.4         | 0.3000  | 0.3000  | 0.3000  |                         |
| 0.5         | 0.4000  | 0.4000  | 0.4000  |                         |
| 0.6         | 1.0000  | 1.0000  | 1.0000  |                         |
| 0.7         | 1.0000  | 1.0000  | 1.0000  |                         |
| 0.8         | 1.4650  | 1.4650  | 1.4650  |                         |
| 0.9         | 1.4650  | 1.4650  | 1.4650  |                         |
| 1.0         | 1.4650  | 1.4650  | 1.4650  |                         |
| 1.1         | 1.4650  | 1.4650  | 1.4650  |                         |
| 1.2         | 1.4650  | 1.4650  | 1.4650  |                         |
| 1.3         | 1.4650  | 1.4650  | 1.4650  |                         |
| 1.4         | 1.4650  | 1.4650  | 1.4650  |                         |
| 1.5         | 1.4650  | 1.4650  | 1.4650  |                         |
| 1.6         | 1.4650  | 1.4650  | 1.4650  |                         |
| 1.7         | 1.4650  | 1.4650  | 1.4650  |                         |
| 1.8         | 1.4650  | 1.4650  | 1.4650  |                         |
| 1.9         | 1.4650  | 1.4650  | 1.4650  |                         |
| 2.0         | 1.4650  | 1.4650  | 1.4650  |                         |
2.	Extract the Final Redemption Formula
	•	Locate and extract the entire text describing the “Final Redemption Formula.”
	•	This text should include the payoff conditions based on the Final Reference Price (also referred to as Final Level).
	3.	Identify Key Conditions
From the extracted formula, identify the following conditions (assuming Par = 1 and Barrier Level = 0.6 or 60%):
	1.	Condition 1:
	•	If the Final Reference Price ≥ 80% of the Initial Reference Price:
Payoff = 146.5% of Par = 1.465
	•	Apply this payoff for Final Level values ≥ 0.8.
	2.	Condition 2:
	•	If the Final Reference Price ≥ Barrier Level (0.6) and < 80%:
Payoff = 100% of Par = 1.0
	•	Apply this payoff for Final Level values from 0.6 (inclusive) up to 0.8 (exclusive).
	3.	Condition 3:
	•	If the Final Reference Price < Barrier Level (0.6):
Payoff = Par × (Final Reference Price / Initial Reference Price) = Final Level
	•	Apply this payoff for Final Level values from 0.0 up to 0.6 (exclusive).
	4.	Plot the Payoffs
	•	For each Final Level from the reference table (0.0, 0.1, 0.2, …, up to 2.0):
	1.	Check which condition applies.
	2.	Assign the corresponding payoff value.
	3.	Populate the Payoff column in the table.
	5.	Sum of Conditions (If Applicable)
	•	If the formula requires summing contributions from multiple conditions (in more complex structures), ensure that each Final Level’s payoff is computed accordingly.
	•	In most standard payoff structures, only one condition applies at a time, so verify if overlapping conditions exist or not.
	6.	Generate the Output
	•	After computing payoffs for each Final Level, output the results in a structured format (e.g., CSV, JSON, or DataFrame).
	•	Example JSON structure:
{
  "PayoffTable": [
    {"FinalLevel": 0.1, "Payoff": 0.1000},
    {"FinalLevel": 0.2, "Payoff": 0.2000},
    ...
    {"FinalLevel": 0.8, "Payoff": 1.4650},
    {"FinalLevel": 0.9, "Payoff": 1.4650},
    ...
    {"FinalLevel": 2.0, "Payoff": 1.4650}
  ]
}
7.	Validation
	•	Double-check that each Final Level has been assigned a single correct payoff according to the specified condition ranges.
	•	Ensure that barrier levels, percentages, and payoff multiples align with the extracted “Final Redemption Formula.”
	8.	Finalize
	•	Present or store the final table with populated payoffs in the desired output format.
	•	Confirm that the payoff calculations align with the logic provided and the reference table values.