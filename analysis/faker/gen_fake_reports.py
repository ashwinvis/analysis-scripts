"""
Created by nuffer at 3/23/20

"""
import time
import uuid
import random
from datetime import datetime, timedelta
from analysis.utils.db import IndividualReportModel, Comorbid
from analysis.utils.db import LocationModel
from analysis.utils.db import session
from analysis.utils import db_enum as enum

def get_npa_list():
    q = session.query(LocationModel)
    locations = q.all()
    geo_locations = []
    for location in locations:
        geo_locations.append(str(location.postal_code))
    return geo_locations


def random_list_element(_list):
    return _list[random.randint(0, len(_list) - 1)]

DAY_FORMAT = '%Y-%m-%d'


def gen_fake_person_list(size: int):
    person_list = []
    npa_list = get_npa_list()
    for n in range(0,size):
        person_list.append({
            'npa': random_list_element(npa_list),
            'session_id': str(uuid.uuid4())
        })
    return person_list


def insert_fake_inidividual_reports():
    from_day = '2020-03-10'
    to_day = '2020-03-15'
    sample_per_day = 1000
    person_list = gen_fake_person_list(sample_per_day)

    from_date = datetime.strptime(from_day, DAY_FORMAT)
    to_date = datetime.strptime(to_day, DAY_FORMAT)

    _from = int(datetime.strptime(from_day, DAY_FORMAT).timestamp())
    _to = int(datetime.strptime(to_day, DAY_FORMAT).timestamp())

    def random_bool():
        return random.randint(0, 1)

    current_day = from_date
    while current_day <= to_date:

        timestamp = current_day.timestamp()
        start_time = time.time()

        for sample in range(0, sample_per_day):
            person = random_list_element(person_list)

            doc_id = str(uuid.uuid4())[0:20]
            
            has_comorbid = random_bool()
            comorbid = Comorbid(
                hypertension = random_bool(),
                cardiovascular = random_bool(),
                pulmonary = random_bool(),
                cancer = random_bool(),
                diabetes = random_bool(),
                renal = random_bool(),
                neurological = random_bool(),
                respiratory = random_bool(),
            )
            report = IndividualReportModel(
                # Metadata
                document_id=doc_id,
                diagnostic=random.randint(0, 4),
                locator=person['npa'],
                session_id=person['session_id'],
                timestamp=(timestamp + sample ) * 1000,  # to millisecond
                analysis_done=False,
                # Actual data
                temp=enum.Scale3(random.randint(1, 3)).name,
                cough=enum.Scale4(random.randint(0, 3)).name,
                breathless=enum.Scale4(random.randint(0, 3)).name,
                energy=enum.Energy(random.randint(0, 4)).name,
                exposure=enum.Exposure(random.randint(0, 2)).name,
                has_comorbid=has_comorbid,
                comorbid=comorbid,
                compromised_immune=random_bool(),
                age=enum.Scale3(random.randint(1, 3)).name,
            )
            # print(report.timestamp)
            session.add(report)

        session.commit()
        spend_time = time.time() - start_time
        print(str(current_day) + ': uploaded ' + str(sample_per_day) + ' samples in ' + str(spend_time) + 's')
        current_day = current_day + timedelta(days=1)


if __name__ == '__main__':

   insert_fake_inidividual_reports()







