import boto3
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    now = datetime.now(timezone.utc)
    one_year_ago = now - timedelta(days=365)

    try:
        # Retrieve all snapshots owned by this account
        response = ec2.describe_snapshots(OwnerIds=['self'])
        snapshots = response.get('Snapshots', [])
        logger.info(f"Found {len(snapshots)} snapshots.")

        for snapshot in snapshots:
            snapshot_id = snapshot['SnapshotId']
            start_time = snapshot['StartTime']

            if start_time < one_year_ago:
                try:
                    logger.info(f"Deleting snapshot: {snapshot_id} (StartTime: {start_time})")
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                except Exception as e:
                    logger.error(f"Error deleting snapshot {snapshot_id}: {e}")
            else:
                logger.info(f"Skipping snapshot: {snapshot_id} (StartTime: {start_time})")
    except Exception as e:
        logger.error(f"Error retrieving snapshots: {e}")