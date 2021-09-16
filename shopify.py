import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

class shoe_data():

	def __init__(self):

		temp_data = pd.read_excel("2019 Winter Data Science Intern Challenge Data Set.xlsx")
		temp_data[["order_id", "shop_id", "user_id", "order_amount", "total_items"]] = temp_data[["order_id", "shop_id", "user_id", "order_amount", "total_items"]].apply(pd.to_numeric)
		temp_data["created_at"] = temp_data["created_at"].apply(pd.to_datetime)

		self.data = temp_data

	def get_data(self):
		return self.data

	def poor_aov(self):

		order_sum = self.data["order_amount"].sum()
		order_len = self.data.shape[0]
		
		aov = order_sum / order_len
		return round(aov, 2)

	def good_aov(self):

		order_sum = self.data["order_amount"].sum()
		item_sum = self.data["total_items"].sum()
		
		aov = order_sum / item_sum
		return round(aov, 2)

	def average_daily_items_sold(self):

		item_sum = self.data["total_items"].sum()
		start_date = self.data["created_at"].min()
		end_date = self.data["created_at"].max()
		date_range = (end_date - start_date).round("1d").days

		adt = item_sum / date_range
		return round(adt, 2)

	def average_daily_revenue(self):

		aov = self.good_aov()
		adt = self.average_daily_items_sold()

		adr = aov * adt
		return round(adr, 2)

	def plot_daily_items_sold(self):

		temp_data = self.data.copy()
		temp_data["created_at"] = temp_data["created_at"].dt.day

		daily_data = temp_data.groupby(["created_at"]).agg({"total_items": "sum"})
		adt = self.average_daily_items_sold()

		plt.plot(daily_data)
		plt.axhline(y=adt, color="r")
		plt.xlabel("Days during March, 2017")
		plt.ylabel("Number of Items Sold")
		plt.title("Daily Items Sold during March, 2017")
		plt.show()

	def plot_daily_revenue(self):

		temp_data = self.data.copy()
		temp_data["created_at"] = temp_data["created_at"].dt.day

		daily_data = temp_data.groupby(["created_at"]).agg({"order_amount": "sum"})
		adr = self.average_daily_revenue()

		plt.plot(daily_data)
		plt.axhline(y=adr, color="r")
		plt.xlabel("Days during March, 2017")
		plt.ylabel("Revenue ($)")
		plt.title("Revenue per Day during March, 2017")
		plt.show()

	def pivot_data(self):

		start_date = self.data["created_at"].min()
		end_date = self.data["created_at"].max()
		date_range = (end_date - start_date).round("1d").days

		new_data = self.data.groupby(["shop_id"], as_index=False).agg({"order_amount": "sum", "total_items": "sum", "user_id": "nunique"})
		new_data.rename(columns={"user_id": "user_count"}, inplace=True)

		new_data["AOV"] = new_data.apply(lambda row: round(row["order_amount"] / row["total_items"], 2), axis=1)
		new_data["ADT"] = new_data.apply(lambda row: round(row["total_items"] / date_range, 2), axis=1)
		new_data["ADR"] = new_data.apply(lambda row: round(row["AOV"] * row["ADT"], 2), axis=1)

		new_data.to_excel("2019 Winter Data Science Intern Challenge Data Set (Per Shop).xlsx", header=True, index=False)


def main():
	data = shoe_data()
	print(data.poor_aov())
	print(data.good_aov())
	print(data.average_daily_items_sold())
	print(data.average_daily_revenue())
	data.pivot_data()
	data.plot_daily_items_sold()
	data.plot_daily_revenue()

if __name__ == "__main__":
	main()

