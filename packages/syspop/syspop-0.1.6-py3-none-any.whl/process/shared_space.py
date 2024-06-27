
from pandas import DataFrame, merge, concat
from scipy.spatial.distance import cdist

def shared_space_wrapper(
        shared_space_name: str,
        shared_space_data: DataFrame, 
        pop_data: DataFrame,
        address_data: DataFrame,
        geography_location_data: DataFrame,
        num_nearest: int = 3,
        assign_address_flag: bool = False):
    """Create synthetic shared space data

    Args:
        shared_space_data (DataFrame): shared space data such as supermarket
        pop_data (DataFrame): population data to be updated
        geography_location_data (DataFrame): geography data
    """

    shared_space_data = shared_space_data.rename(
        columns={
            "latitude": f"latitude_{shared_space_name}", 
            "longitude": f"longitude_{shared_space_name}", 
            "name": shared_space_name}
    )

    shared_space_data = shared_space_data.drop(columns=["area"])

    pop_data = merge(pop_data, geography_location_data, on="area", how="left")

    for i in range(num_nearest):

        if i == 0:
            distance_matrix = cdist(
                pop_data[["latitude", "longitude"]], 
                shared_space_data[[f"latitude_{shared_space_name}", f"longitude_{shared_space_name}"]], 
                metric="euclidean")
        else:
            distance_matrix[range(len(nearest_indices)), nearest_indices] = float('inf')

        nearest_indices = distance_matrix.argmin(axis=1)
        nearest_rows = shared_space_data.iloc[nearest_indices].reset_index(drop=True)

        nearest_rows.rename(columns={shared_space_name: f"tmp_{i}"}, inplace=True)

        pop_data = concat([pop_data, nearest_rows], axis=1)

        pop_data = pop_data.drop(
            columns=[f"latitude_{shared_space_name}", f"longitude_{shared_space_name}"])
        
    # Loop through the columns and combine them
    for i in range(num_nearest):
        pop_data[shared_space_name] = pop_data.get(shared_space_name, "") + pop_data[f"tmp_{i}"].astype(str) + ","
        pop_data = pop_data.drop(columns=[f"tmp_{i}"])

    pop_data[shared_space_name] = pop_data[shared_space_name].str.rstrip(",")
    pop_data = pop_data.drop(columns=["latitude", "longitude"])

    if assign_address_flag:
        address_data = add_shared_space_address(
            pop_data, 
            shared_space_data, 
            address_data, 
            shared_space_name)

    return pop_data, address_data


def add_shared_space_address(pop_data: DataFrame, shared_space_data: DataFrame, address_data: DataFrame, shared_space_name: str) -> DataFrame:
    """Add shared space address

    Args:
        shared_space_data (DataFrame): _description_
        address_data (DataFrame): _description_

    Returns:
        DataFrame: Updated address dataset
    """
    unique_shared_space = list(set(pop_data[shared_space_name].str.split(',').explode()))

    # get the lat/lon for unique shared space
    unique_shared_space = (
        shared_space_data[
            shared_space_data[shared_space_name].apply(
                lambda x: any(item in x for item in unique_shared_space))]).drop_duplicates()

    unique_shared_space = unique_shared_space.rename(columns={
        shared_space_name: "name",
        f"latitude_{shared_space_name}": "latitude",
        f"longitude_{shared_space_name}": "longitude"
    })

    unique_shared_space["type"] = shared_space_name

    return concat([address_data, unique_shared_space])
