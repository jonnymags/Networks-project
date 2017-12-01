import json
import sys


def clean_businesses(business_file):
	business_ids = {}
	outfile = "lv_businesses.txt"
	with open(outfile, "wb") as o:
		with open(business_file, "rb") as f:
			for line in f:
				j = json.loads(line)
				if j["city"] == "Las Vegas" and "Food" in j["categories"]:
					o.write(line)
					business_ids[j["business_id"]] = 0

	return business_ids

def clean_reviews(review_file, business_ids):
	outfile = "lv_reviews.txt"
	with open(outfile, "wb") as o:
		with open(review_file, "rb") as f:
			for line in f:
				j = json.loads(line)
				if j["business_id"] in business_ids:
					o.write(line)	

def main():
	try:
		review_file = sys.argv[1]
		business_file = sys.argv[2]
	except IndexError as e:
		print("Must provide input file.")
		sys.exit(-1)

	business_ids = clean_businesses(business_file)
	clean_reviews(review_file, business_ids)



if __name__ == "__main__":
	main()