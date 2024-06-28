import os
import time
import cloudpickle as pickle
import pandas as pd
from datetime import datetime, timedelta, timezone



class TimeTravelLoaderMixin:
    """
    Enables Retrieval of Objects across time range from serving models.
    """
    def __init__(self,
                 *args,
                 **kwargs):
        self.keys_to_exclude = ("score_func.pkl",)

    def load_from_time(self,
                       ml_model_id: str,
                       ml_version_id: str,
                       from_timestamp: datetime,
                       to_timestamp: datetime,
                       add_data_to_catalog: bool = False,
                       file_name: str = None,
                       model_path: str = None,
                       ):
        """
        This will retrieve payloads and valid payload from selected time frame.

        :param ml_model_id: Model Id String
        :param ml_version_id: Version Id String
        :param from_timestamp: From TimeStamp Must Be Timezone Aware (UTC) ex: datetime.now(timezone.utc)
        :param to_timestamp:  To TimeStamp Must Be Timezone Aware (UTC) ex: datetime.now(timezone.utc)
        :param add_data_to_catalog:
            if True data will be persisted in Mosaic AI DATA Section.
            Requires tabulate=True at Init.
            Note: This will first download data into your workspace.
        :param file_name:
            If Provided Will Upload Data With Same Name in Mosaic AI Data Catalog.
            Requires tabulate=True at Init.
        :param model_path: mount path for model data
        :return: Bool
        """
        self.model_dir_path = f"{model_path}/{ml_model_id}/{ml_version_id}/"
        self.all_keys = os.listdir(self.model_dir_path)
        self.only_pickled_objects = [objects_ for objects_ in self.all_keys if objects_.endswith("pkl")
                                     and not objects_.endswith(self.keys_to_exclude)]

        # loading files based on it's last modified time
        self.keys_to_load = [pickled_items for pickled_items in self.only_pickled_objects \
                             if from_timestamp <=  time.ctime(os.path.getmtime(os.path.join(self.model_dir_path, pickled_items))) <= to_timestamp]


        self.temp_score_collection_ = []

        for item in self.keys_to_load:
            self.temp_score_collection_ \
                .extend(pickle.load(open(os.path.join(self.model_dir_path, item), "rb")))

        self.add_response(score_response=self.temp_score_collection_)

        if add_data_to_catalog and self.tabulate_frame is not None:
            from connector.mosaicio import MosaicioConnector
            self.io_connector = MosaicioConnector()
            name = file_name or "{}_{}.csv".format(datetime.strptime(from_timestamp, '%Y_%m_%d'),
                                                    datetime.strptime(to_timestamp, '%Y_%m_%d'))
            self.tabulate_frame.to_csv(name, index=False)
            self.io_connector.upload(name)


        return True
