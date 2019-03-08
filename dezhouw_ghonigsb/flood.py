# flood.py
# created on Feb 27, 2019

import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import ssl
import sys
import traceback
import csv
import xmltodict
import io

class flood(dml.Algorithm):
	contributor = "dezhouw_ghonigsb"
	reads       = []
	writes      = ["nine_inch_sea_level_rise_1pct_annual_flood",
				   "nine_inch_sea_level_rise_high_tide",
				   "thirty_six_inch_sea_level_rise_high_tide",
				   "thirty_six_inch_sea_level_rise_10_pct_annual_flood",
				   "zoning_subdistricts",
				   "zillow_boston_neighborhood"]

	@staticmethod
	def execute(trial = False):
		startTime = datetime.datetime.now()

		# Set up the database connection.
		client = dml.pymongo.MongoClient()
		repo   = client.repo
		repo.authenticate("dezhouw_ghonigsb", "dezhouw_ghonigsb")

		# Drop all collections
		collection_names = repo.list_collection_names()
		for collection_name in collection_names:
			repo.dropCollection(collection_name)

		# nine_inch_sea_level_rise_1pct_annual_flood
		collection_name = "nine_inch_sea_level_rise_1pct_annual_flood"
		url             = "https://opendata.arcgis.com/datasets/74692fe1b9b24f3c9419cd61b87e4e3b_7.geojson"
		gcontext        = ssl.SSLContext()
		response        = urllib.request.urlopen(url, context=gcontext).read().decode("utf-8")
		r               = json.loads(response)
		repo.createCollection(collection_name)
		repo["dezhouw_ghonigsb."+collection_name].insert_one(r)
		print("Success: [{}]".format(collection_name))

		# nine_inch_sea_level_rise_high_tide
		collection_name = "nine_inch_sea_level_rise_high_tide"
		url             = "https://opendata.arcgis.com/datasets/74692fe1b9b24f3c9419cd61b87e4e3b_8.geojson"
		gcontext        = ssl.SSLContext()
		response        = urllib.request.urlopen(url, context=gcontext).read().decode("utf-8")
		r               = json.loads(response)
		repo.createCollection(collection_name)
		repo["dezhouw_ghonigsb."+collection_name].insert_one(r)
		print("Success: [{}]".format(collection_name))

		# thirty_six_inch_sea_level_rise_high_tide
		collection_name = "thirty_six_inch_sea_level_rise_high_tide"
		url             = "https://opendata.arcgis.com/datasets/74692fe1b9b24f3c9419cd61b87e4e3b_8.geojson"
		gcontext        = ssl.SSLContext()
		response        = urllib.request.urlopen(url, context=gcontext).read().decode("utf-8")
		r               = json.loads(response)
		repo.createCollection(collection_name)
		repo["dezhouw_ghonigsb."+collection_name].insert_one(r)
		print("Success: [{}]".format(collection_name))

		# thirty_six_inch_sea_level_rise_10_pct_annual_flood
		collection_name = "thirty_six_inch_sea_level_rise_10_pct_annual_flood"
		url             = "https://opendata.arcgis.com/datasets/74692fe1b9b24f3c9419cd61b87e4e3b_3.geojson"
		gcontext        = ssl.SSLContext()
		response        = urllib.request.urlopen(url, context=gcontext).read().decode("utf-8")
		r               = json.loads(response)
		repo.createCollection(collection_name)
		repo["dezhouw_ghonigsb."+collection_name].insert_one(r)
		print("Success: [{}]".format(collection_name))


		# zoning_subdistricts
		collection_name = "zoning_subdistricts"
		url             = "https://opendata.arcgis.com/datasets/b601516d0af44d1c9c7695571a7dca80_0.geojson"
		gcontext        = ssl.SSLContext()
		response        = urllib.request.urlopen(url, context=gcontext).read().decode("utf-8")
		r               = json.loads(response)
		repo.createCollection(collection_name)
		repo["dezhouw_ghonigsb."+collection_name].insert_one(r)
		print("Success: [{}]".format(collection_name))

		# census
		collection_name = "zillow_boston_neighborhood"
		params          = {
			'zws-id'   : dml.auth["census"]["Zillow API"]["zws-id"],
			'state'    : 'ma',
			'city'     : 'boston',
			'childtype': 'neighborhood'
		}
		args            = urllib.parse.urlencode(params).encode('UTF-8')
		url             = "https://www.zillow.com/webservice/GetRegionChildren.htm?"
		gcontext        = ssl.SSLContext()
		response        = urllib.request.urlopen(url, args, context=gcontext).read().decode("utf-8")
		r               = xmltodict.parse(response)
		repo.createCollection(collection_name)
		repo["dezhouw_ghonigsb."+collection_name].insert_one(r)
		print("Success: [{}]".format(collection_name))

		# MassGov
		collection_name = "massgov_most_recent_peak_hr"
		url             = "http://datamechanics.io/data/ghonigsb_dezhouw/MostRecentPeakHrByYearVolume.csv"
		response        = urllib.request.urlopen(url).read().decode("utf-8")
		fieldnames      = ['local_id','dir','seven_to_eight','seven_to_nine','eleven_to_two','three_to_six','five_to_six','offpeak','daily','latitude','longitude','start_date','hpms_loc','daily1','aadt','on_road','approach','at_road']
		reader          = csv.DictReader(io.StringIO(response), fieldnames)
		next(reader, None) # skip header
		repo.createCollection(collection_name)
		for row in reader:
			repo["dezhouw_ghonigsb."+collection_name].insert_one(row)
		print("Success: [{}]".format(collection_name))

        # Disconnect database for data safety
		repo.logout()

		endTime = datetime.datetime.now()
		return {"start":startTime, "end":endTime}

	@staticmethod
	def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):

		doc.add_namespace('alg', 'http://datamechanics.io/algorithm/')
		doc.add_namespace('dat', 'http://datamechanics.io/data/')
		doc.add_namespace('ont', 'http://datamechanics.io/ontology#')
		doc.add_namespace('log', 'http://datamechanics.io/log/')

		# extra resources
		doc.add_namespace('opd', 'https://opendata.arcgis.com/datasets/')
		doc.add_namespace('zil', 'https://www.zillow.com/webservice/')
		doc.add_namespace('gov', 'http://datamechanics.io/data/ghonigsb_dezhouw/')

		this_script   = doc.agent('alg:dezhouw_ghonigsb#flood', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
		resource1     = doc.entity('opd:boston', {'prov:label':'Opendata Website', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'geojson'})
		resource2     = doc.entity('zil:boston', {'prov:label':'Zillow API',       prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'xml'})
		resource3     = doc.entity('gov:boston', {'prov:label':'MassGov',          prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'csv'})
		get_seaAnnual = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
		get_seaTide   = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
		get_zoning    = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
		get_zillow    = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
		get_massGov   = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)

		doc.wasAssociatedWith(get_seaAnnual, this_script)
		doc.wasAssociatedWith(get_seaTide,   this_script)
		doc.wasAssociatedWith(get_zoning,    this_script)
		doc.wasAssociatedWith(get_zillow,    this_script)
		doc.wasAssociatedWith(get_massGov,   this_script)

		doc.usage(get_seaAnnual, resource1, startTime, None,
			      {prov.model.PROV_TYPE:'ont:Retrieval',
			      'ont:Query':'?type=Sea+Level+Annual'})
		doc.usage(get_seaTide,   resource1, startTime, None,
			      {prov.model.PROV_TYPE:'ont:Retrieval',
			      'ont:Query':'?type=Sea+High+Tide'})
		doc.usage(get_zoning,    resource1, startTime, None,
			      {prov.model.PROV_TYPE:'ont:Retrieval',
			      'ont:Query':'?type=Zone'})
		doc.usage(get_zillow,    resource2, startTime, None,
			      {prov.model.PROV_TYPE:'ont:Retrieval',
			      'ont:Query':'?type=Boston+Neighborhood'})
		doc.usage(get_massGov,   resource3, startTime, None,
			      {prov.model.PROV_TYPE:'ont:Retrieval',
			      'ont:Query':'?type=Peak+Hours'})

		seaAnnual = doc.entity('dat:dezhouw_ghonigsb#nine_inch_sea_level_rise_1pct_annual_flood',
								{prov.model.PROV_LABEL:'Sea Level Annual',
								 prov.model.PROV_TYPE:'ont:DataSet'})
		doc.wasAttributedTo(seaAnnual, this_script)
		doc.wasGeneratedBy(seaAnnual, get_seaAnnual, endTime)
		doc.wasDerivedFrom(seaAnnual, resource1, get_seaAnnual, get_seaAnnual, get_seaAnnual)

		seaTide   = doc.entity('dat:dezhouw_ghonigsb#nine_inch_sea_level_rise_high_tide',
								{prov.model.PROV_LABEL:'Sea Level High Tide',
								 prov.model.PROV_TYPE:'ont:DataSet'})
		doc.wasAttributedTo(seaTide, this_script)
		doc.wasGeneratedBy(seaTide, get_seaTide, endTime)
		doc.wasDerivedFrom(seaTide, resource1, get_seaTide, get_seaTide, get_seaTide)

		zoning    = doc.entity('dat:dezhouw_ghonigsb#zoning_subdistricts',
								{prov.model.PROV_LABEL:'Zone Subdistricts',
								 prov.model.PROV_TYPE:'ont:DataSet'})
		doc.wasAttributedTo(zoning, this_script)
		doc.wasGeneratedBy(zoning, get_zoning, endTime)
		doc.wasDerivedFrom(zoning, resource1, get_zoning, get_zoning, get_zoning)

		zillow    = doc.entity('dat:dezhouw_ghonigsb#zillow_boston_neighborhood',
								{prov.model.PROV_LABEL:'Boston Neighborhood',
								 prov.model.PROV_TYPE:'ont:DataSet'})
		doc.wasAttributedTo(zillow, this_script)
		doc.wasGeneratedBy(zillow, get_zillow, endTime)
		doc.wasDerivedFrom(zillow, resource1, get_zillow, get_zillow, get_zillow)

		massGov   = doc.entity('dat:dezhouw_ghonigsb#massgov_most_recent_peak_hr',
								{prov.model.PROV_LABEL:'Peak Hours',
								 prov.model.PROV_TYPE:'ont:DataSet'})
		doc.wasAttributedTo(massGov, this_script)
		doc.wasGeneratedBy(massGov, get_massGov, endTime)
		doc.wasDerivedFrom(massGov, resource1, get_massGov, get_massGov, get_massGov)

		return doc

if __name__ == '__main__':
	try:
		print(flood.execute())
		doc = flood.provenance()
		print(doc.get_provn())
		print(json.dumps(json.loads(doc.serialize()), indent=4))
	except Exception as e:
		traceback.print_exc(file = sys.stdout)
	finally:
		print("Safely close")
