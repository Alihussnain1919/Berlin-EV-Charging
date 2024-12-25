import pandas as pd
from core import methods as m1
from core import HelperTools as ht
from config import pdict


@ht.timer
def main():
    """Main: Generation of Streamlit App for visualizing electric charging stations & residents in Berlin"""

    # Load geodata for Berlin PLZ
    try:
        df_geodat_plz = pd.read_csv("datasets/" + pdict["file_geodat_plz"], delimiter=";")
        print("Geodata loaded successfully.")
    except Exception as e:
        print(f"Error loading geodata: {e}")
        return

    # Load charging stations data
    try:
        df_lstat = pd.read_csv("datasets/" + pdict["file_lstations"], delimiter=",")
        print("Charging stations data loaded successfully.")
    except Exception as e:
        print(f"Error loading charging stations data: {e}")
        return
    
    # Preprocess charging stations data
    try:
        df_lstat2 = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)
        print("Charging stations data preprocessed successfully.")
    except Exception as e:
        print(f"Error preprocessing charging stations data: {e}")
        return
    
    # Count occurrences per PLZ
    try:
        gdf_lstat3 = m1.count_plz_occurrences(df_lstat2)
        print("Charging stations occurrences counted.")
    except Exception as e:
        print(f"Error counting charging stations occurrences: {e}")
        return

    # Load residents data
    try:
        df_residents = pd.read_csv("datasets/" + pdict["file_residents"], delimiter=",")
        print("Residents data loaded successfully.")
    except Exception as e:
        print(f"Error loading residents data: {e}")
        return

    # Preprocess residents data
    try:
        gdf_residents2 = m1.preprop_resid(df_residents, df_geodat_plz, pdict)
        print("Residents data preprocessed successfully.")
    except Exception as e:
        print(f"Error preprocessing residents data: {e}")
        return

    # Generate Streamlit app
    try:
        m1.make_streamlit_electric_Charging_resid(gdf_lstat3, gdf_residents2)
        print("Streamlit app created successfully.")
    except Exception as e:
        print(f"Error creating Streamlit app: {e}")


if __name__ == "__main__":
    main()
