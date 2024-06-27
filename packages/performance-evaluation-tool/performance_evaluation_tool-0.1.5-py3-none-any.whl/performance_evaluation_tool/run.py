from performance_evaluation_tool import *
import time
import copy

# Configure logging
logging.basicConfig(level=logging.INFO)
    
def main():
    start_time = time.time()

    # Parse command line arguments
    args, var = parse_args()

    # Check if query and reference image directories are provided
    if var['query_image_dir'] is None or var['reference_image_dir'] is None:
        logging.error("Either Query image directory or Reference image directory is not provided")
        return

    # Retrieve file paths for query and reference images
    query_image_base_dpath = var['query_image_dir']
    reference_image_base_dpath = var['reference_image_dir']
    output_filename = var['output_filename']

    # Create ImageKeys for query and reference images
    query_keys = set(
        [ImageKey(query_image_fpath, query_image_base_dpath)
        for query_image_fpath in glob.glob(f'{query_image_base_dpath}/*.png')])

    reference_keys = set(
        [ImageKey(reference_image_fpath, reference_image_base_dpath)
        for reference_image_fpath in glob.glob(f'{reference_image_base_dpath}/*.png')])

    logging.info(f"Number of images in the query directory: {len(query_keys)}")
    logging.info(f"Number of images in the reference directory: {len(reference_keys)}")

    # Find common images for evaluation
    evaluation_keys = query_keys.intersection(reference_keys)
    logging.info(f"Number of images in the evaluation set: {len(evaluation_keys)}")

    if not evaluation_keys:
        logging.error(f"No common images found in the query and reference directories.")
        return

    # Check if some images in the query directory do not have corresponding images in the reference directory
    if len(evaluation_keys) != len(query_keys) or len(evaluation_keys) != len(reference_keys):
        logging.warning("Some images in the query directory do not have corresponding images in the reference directory.")

    # Create ImageInstances for query and reference images
    queries = {
        eval_key: ImageInstance(eval_key, query_image_base_dpath)
        for eval_key in evaluation_keys}

    references = {
        eval_key: ImageInstance(eval_key, reference_image_base_dpath)
        for eval_key in evaluation_keys}

    # Boolean flag to ignore pixels with specific values
    to_ignore = var['to_ignore']
    if to_ignore:
        logging.info(f"Ignoring pixels with values: {[255, 255, 255]}")

    # Perform Evaluation
    match_calculator = SemanticSegmentationMatchCalculator(to_ignore = to_ignore, ignore_pixels=[255, 255, 255])
    summarizer = SummarizeMetrics()

    matches = {}
    confusion_matrix = {}
    per_image_matches = {}
    per_image_confusion_matrix = {}
    for key in evaluation_keys:
        query = queries[key]
        reference = references[key]
        match_result, confusion_matrix_result = match_calculator.match(query, reference)

        # Create a deep copy of the match_result to avoid overwriting it
        match_result_copy = copy.deepcopy(match_result)
        confusion_matrix_result_copy = copy.deepcopy(confusion_matrix_result)
        
        # Append match results to per_image_matches and Add match results to matches
        matches = dict_matches_adder(matches, match_result_copy)
        per_image_matches = dict_matches_appender(per_image_matches, match_result, key)

        # Append confusion_matrix_result to per_image_confusion_matrix and Add confusion_matrix_results to confusion_matrix
        confusion_matrix = dict_matches_adder(confusion_matrix, confusion_matrix_result_copy)
        per_image_confusion_matrix = dict_matches_appender(per_image_confusion_matrix, confusion_matrix_result, key)

    # Summarize metrics
    summarizer.summarize(matches, per_image_matches, confusion_matrix, per_image_confusion_matrix, output_filename)
    logging.info("Main function execution completed.")
    logging.info(f"Execution time: {time.time() - start_time} seconds")

if __name__ == "__main__":
    main()
