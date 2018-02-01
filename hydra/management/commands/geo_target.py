from django.core.management.base import BaseCommand
from bsd.models import ConstituentAddress
from django.contrib.gis.geos import Point, GEOSGeometry
import logging
import json
import csv

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Take a geojson file and state abbreviation and generate a\
    list of BSD constituent IDs inside those boundaries'

    def add_arguments(self, parser):
        parser.add_argument('geojson_file')
        parser.add_argument('state')

    def handle(self, *args, **options):
        logger.debug('Running geo_target.py')

        cons_ids = []
        kwargs = {
            'state_cd': options['state'],
            'is_primary': True
        }

        with open(options['geojson_file']) as data_file:
            geojson = json.load(data_file)

        # Get all constituent addresses in the state
        cons_addrs = ConstituentAddress.objects.filter(**kwargs)

        if geojson['type'] == 'FeatureCollection':
            # todo: fetch number, but stick to 1st for now
            geojson = geojson['features'][0]['geometry']

        poly = GEOSGeometry(json.dumps(geojson))

        for con in cons_addrs:
            point = Point(y=con.latitude, x=con.longitude)
            if poly.contains(point):
                cons_ids.append(con.cons_id)

        with open('./cons-ids.csv', 'wb') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(cons_ids)

        logger.debug('Geo targetting finished. Check ./cons-ids.csv')
