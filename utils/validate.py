def validate_dataset(df, name):
    print("\n" + "=" * 50)
    print(f"{name} DATASET")
    print("=" * 50)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nData Types:")
    print(df.dtypes)