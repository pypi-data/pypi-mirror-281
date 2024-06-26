# Batch Processor Custom

This package provides an efficient solution for batch processing of data in MongoDB collections. It enables reading, locking, processing, and unlocking records in batches, facilitating the management and scalable processing of large data volumes.

## Features

- Configurable connection to any MongoDB instance.
- Efficient handling of record locking and unlocking to ensure data integrity during batch processing.
- Ability to process batches of specified size, suitable for large-scale data operations.

## Installation

You can install this package using pip:

```bash
pip install batch_processor_custom

## Usage


from batch_processor_custom import BatchProcessor

# Initialize the processor
processor = BatchProcessor('mongodb://localhost:27017', 'your_database', 'your_collection')

# Process batches
for batch_id, records in processor.process_batches(10, 100):
    print(f'Processing batch {batch_id}')
    # Here you can add your processing logic
    processor.unlock_records([record['_id'] for record in records])

##License

This project is licensed under the MIT License - see the LICENSE file for details.

