import asyncio
from panoramisk import Manager

from pg_db import *

manager = Manager(loop=asyncio.get_event_loop(),
                  host='192.168.0.110',
                  username='adminconf',
                  secret='58a3d20cc970b350f4c8ef5294c988dc')


@manager.register_event('ConfbridgeStart')
def callback(manager, message):
    print('New conference:',
          message['Conference'],
          message['BridgeUniqueid'],
          message['BridgeName'])

    create_tables(message['Conference'],
                  message['BridgeUniqueid'],
                  message['BridgeName'])


@manager.register_event('ConfbridgeEnd')
def callback(manager, message):
    print('The conference is over:',
          message['Conference'],
          message['BridgeName'],
          message['BridgeUniqueid'])


@manager.register_event('BridgeEnter')
def callback(manager, message):
    print('New participant:',
          message['BridgeUniqueid'],
          message['BridgeName'],
          message['Channel'],
          message['CallerIDNum'],
          message['CallerIDName'])

    join_participants(message['BridgeUniqueid'],
                      message['BridgeName'],
                      message['Channel'],
                      message['CallerIDNum'],
                      message['CallerIDName'])


@manager.register_event('ConfbridgeJoin')
def callback(manager, message):
    print('New participant join:',
          message['BridgeUniqueid'],
          message['BridgeName'],
          message['Channel'],
          message['CallerIDNum'],
          message['CallerIDName'],
          message['Admin'])

    join_participants(message['BridgeUniqueid'],
                      message['BridgeName'],
                      message['Channel'],
                      message['CallerIDNum'],
                      message['CallerIDName'],
                      message['Admin'])


@manager.register_event('ConfbridgeTalking')
def callback(manager, message):
    print('Microphone on/off:',
          message['BridgeUniqueid'],
          message['Conference'],
          message['BridgeName'],
          message['Channel'],
          message['CallerIDNum'],
          message['CallerIDName'],
          message['TalkingStatus'],
          message['Admin'])

    join_participants(message['BridgeUniqueid'],
                      message['BridgeName'],
                      message['Channel'],
                      message['CallerIDNum'],
                      message['CallerIDName'],
                      message['TalkingStatus'],
                      message['Admin'])


@manager.register_event('ConfbridgeLeave')
def callback(manager, message):
    print('Confbridge Leave:',
          message['BridgeUniqueid'],
          message['Conference'],
          message['BridgeName'],
          message['Channel'],
          message['CallerIDNum'],
          message['CallerIDName'],
          message['Admin'])

    delete_participants(message['BridgeUniqueid'],
                        message['BridgeName'],
                        message['Channel'],
                        message['CallerIDNum'],
                        message['CallerIDName'],
                        message['Admin'])


@manager.register_event('BridgeLeave')
def callback(manager, message):
    print('BridgeLeave:',
          message['BridgeUniqueid'],
          message['BridgeName'],
          message['Channel'],
          message['CallerIDNum'],
          message['CallerIDName'])

    delete_participants(message['BridgeUniqueid'],
                        message['BridgeName'],
                        message['Channel'],
                        message['CallerIDNum'],
                        message['CallerIDName'])


@manager.register_event('BridgeDestroy')
def callback(manager, message):
    print('BridgeLeave:',
          message['BridgeUniqueid'],
          message['BridgeName'],
          message['BridgeNumChannels'])

    delete_conference(message['BridgeUniqueid'],
                      message['BridgeName'])


def write_log_in_file(message):
    file = open('browsers.txt', 'a')
    file.write(str(message)+"\n")
    file.close()


def main():
    manager.connect()
    try:
        manager.loop.run_forever()
    except KeyboardInterrupt:
        manager.loop.close()


if __name__ == '__main__':
    main()