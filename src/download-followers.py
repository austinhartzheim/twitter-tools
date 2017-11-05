#! /usr/bin/env python3
import csv
import json
import time
import argparse

import twitter

import config
import libs.headers

MAX_FOLLOWERS_PER_REQUEST = 200


class Main():
    def __init__(self, args):
        self.args = args

    def lookup_user(self, api):
        '''
        :param api twitter.Twitter: Twitter API object.
        '''
        users = api.users.lookup(screen_name=self.args.username)
        if len(users) < 1:
            print('Error: Could not find that username')
            exit(1)
        elif len(users) > 1:
            print('Error: Found more than one user')
            exit(1)

        return users[0]

    def create_api_connection(self):
        auth = twitter.OAuth(config.access_token, config.access_token_secret,
                             config.consumer_key, config.consumer_secret)
        return twitter.Twitter(auth=auth, retry=True)

    def download_followers(self, api, writer):
        page = {'next_cursor': -1}
        downloaded_users = 0

        while page['next_cursor'] != 0:
            page = api.followers.list(screen_name=self.args.username,
                                      count=MAX_FOLLOWERS_PER_REQUEST,
                                      cursor=page['next_cursor'])


            for user in page['users']:
                csv_row_output = []

                # Get the expanded version of the t.co URL.
                if user['url']:
                    user['url'] = user['entities']['url']['urls'][0]['expanded_url']
            
                for field in libs.headers.full:
                    if field in user:
                        csv_row_output.append(user[field])
                    else:
                        csv_row_output.append(None)

                writer.writerow(csv_row_output)
                downloaded_users += 1
                print(' - Downlaoded %s' % user['name'])
                    

    def run(self):
        writer = csv.writer(self.args.outfile)
        writer.writerow(libs.headers.full)

        api = self.create_api_connection()
        user = self.lookup_user(api)

        total_followers = user['followers_count']
        print('Fetching followers for user: %s' % user['name'])
        print(' - Total Followers: %i' % user['followers_count'])

        self.download_followers(api, writer)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('username')
    parser.add_argument('outfile', type=argparse.FileType('w'))
    args = parser.parse_args()

    main = Main(args)
    main.run()
