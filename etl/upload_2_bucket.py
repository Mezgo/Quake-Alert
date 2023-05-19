
from google.cloud import storage
from Funciones_ETL import carga

PROJECT_ID = 'quake-alert-e44c3'
BUCKET = 'buket-geodata'


def authenticate_implicit_with_adc(project_id):
    """
    When interacting with Google Cloud Client libraries, the library can auto-detect the
    credentials to use.

    // TODO(Developer):
    //  1. Before running this sample,
    //  set up ADC as described in https://cloud.google.com/docs/authentication/external/set-up-adc
    //  2. Replace the project variable.
    //  3. Make sure that the user account or service account that you are using
    //  has the required permissions. For this sample, you must have "storage.buckets.list".
    Args:
        project_id: The project id of your Google Cloud project.
    """

    # This snippet demonstrates how to list buckets.
    # *NOTE*: Replace the client created below with the client required for your application.
    # Note that the credentials are not specified when constructing the client.
    # Hence, the client library will look for credentials using ADC.
    storage_client = storage.Client(project=project_id)
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")


# authenticate_implicit_with_adc(PROJECT_ID)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


def upload_to_bucket():

    """Sube al bucket del proyecto los datos en bruto
    de las distintas fuentes de datos sismicos de los
    paises"""

    # Carga de datos de japon
    japon = carga.japon()
    file_japon = japon.history().name
    name = file_japon.split('/')[-1]
    print(name)
    upload_blob(BUCKET, file_japon, name)

    # Carga de datos de eeuu
    # eeuu = carga.eeuu()
    # file_eeuu = eeuu.history().name
    # name = file_eeuu.split('/')[-1]
    # print(name)
    # upload_blob(BUCKET, file_eeuu, name)

    # # Carga de datos de chile
    # chile = carga.chile()
    # file_chile = chile.history().name
    # name = file_chile.split('/')[-1]
    # print(name)
    # upload_blob(BUCKET, file_chile, name)


upload_to_bucket()
