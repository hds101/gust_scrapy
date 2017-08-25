# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from gust_scrapy.models import GustCompany, GustUser, db_connect, create_table


class PgPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()

        company = session.query(GustCompany).filter_by(url=item['company']['url']).first()
        if not company:
            company = GustCompany(**item['company'])
            session.add(company)

        user = session.query(GustUser).filter_by(url=item['user']['url']).first()
        if not user:
            company.gust_users.append(GustUser(**item['user']))

        try:
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
