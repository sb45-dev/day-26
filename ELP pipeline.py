import pandas as pd
import json
import logging


# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -----------------------------
# Load Configuration
# -----------------------------
def load_config():
    with open("config.json", "r") as file:
        config = json.load(file)

    logging.info("Configuration loaded")
    return config


# -----------------------------
# Extract
# -----------------------------
def extract_data(input_file):
    print("Reading input data...")

    data = pd.read_csv(input_file)

    logging.info("Data extracted successfully")
    print("Input rows:", len(data))

    return data


# -----------------------------
# Validate
# -----------------------------
def validate_data(data, required_columns):

    print("\nValidating data...")

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(
                f"Required column missing: {column}"
            )

    print("Validation successful!")
    logging.info("Data validation successful")


# -----------------------------
# Transform
# -----------------------------
def transform_data(data, transformations):

    print("\nTransforming data...")

    # Fill missing values
    if transformations["fill_missing"]:
        data = data.fillna(0)

    # Remove duplicate records
    if transformations["remove_duplicates"]:
        data = data.drop_duplicates()

    # Salary filter
    minimum_salary = transformations["minimum_salary"]

    data = data[data["Salary"] >= minimum_salary]

    logging.info("Data transformation completed")

    return data


# -----------------------------
# Load
# -----------------------------
def load_data(data, output_file):

    data.to_csv(output_file, index=False)

    print("\nFinal data saved to:", output_file)
    logging.info("Final data loaded successfully")


# -----------------------------
# Main ETL Pipeline
# -----------------------------
def main():

    print("================================")
    print("   CONFIGURATION DRIVEN ETL")
    print("================================")

    try:

        # Load configuration
        config = load_config()

        # Extract
        data = extract_data(
            config["input_file"]
        )

        # Save raw data
        data.to_csv("raw_data.csv", index=False)

        # Validate
        validate_data(
            data,
            config["required_columns"]
        )

        # Transform
        data = transform_data(
            data,
            config["transformations"]
        )

        # Save transformed data
        data.to_csv(
            "transformed_data.csv",
            index=False
        )

        # Load final data
        load_data(
            data,
            config["output_file"]
        )

        print("\nETL Pipeline completed successfully!")
        print("Final records:", len(data))

    except Exception as error:

        print("\nPipeline failed!")
        print("Error:", error)

        logging.error(
            f"Pipeline failed: {error}"
        )


# Run program
if __name__ == "__main__":
    main()