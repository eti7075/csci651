import logging

def get_logger(name="P2P"):
    """
    creates and returns a configured logger for the UI of the program

    :param name: name of the program/app
    :type name: string
    :return: logger
    :rtype: logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add handlers
    if not logger.handlers:
        logger.addHandler(ch)

    return logger

def format_file_chunks(files):
    """
    helper function to format the output for the files store in local memory on a peer
    this is not really a logger function, but is used in output
    
    :param files: files and chunks to output
    :type files: map<string, map<string, string>>
    :return: files and the number of chunks available in string format
    :rtype: string
    """
    output = "\n"
    for file, chunk in files.items():
        output += f"{file} chunks available: {[key for key, value in chunk.items()]}\n"
    return output
