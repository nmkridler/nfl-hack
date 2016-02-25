def convert_index_to_str(df):
    """
        This function takes in a dataframe
        that has a column called play_index and
        converts it to a string

    """
    df["play_index"] = df["play_index"].astype("str")
    return df

FILES = {
    "local": {
        "on_field": {
            "name": "pyxleyapp/static/players_on_field.csv",
            "func": convert_index_to_str
        },
        "off_field": {
            "name": "pyxleyapp/static/players_on_field.csv",
            "func": convert_index_to_str
        },
        "locations": {
            "name": "pyxleyapp/static/locations_of_players.csv",
            "func": convert_index_to_str
        }
    }
}
