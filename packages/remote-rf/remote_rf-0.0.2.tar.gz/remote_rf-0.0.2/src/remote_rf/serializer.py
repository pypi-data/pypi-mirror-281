import torch
import numpy as np
import pickle

def serialize_data(data):
    """
    Serializes PyTorch tensors and NumPy arrays in the data dictionary.

    Parameters:
    data (dict): A dictionary containing PyTorch tensors or NumPy arrays.

    Returns:
    bytes: Serialized data.
    """
    if isinstance(data, dict):
        if 'torch_tensor' in data:
            data['torch_tensor'] = data['torch_tensor'].tolist()
        if 'numpy_array' in data:
            data['numpy_array'] = data['numpy_array'].tolist()
    return pickle.dumps(data)

def deserialize_data(serialized_data):
    """
    Deserializes data and converts lists back to PyTorch tensors and NumPy arrays.

    Parameters:
    serialized_data (bytes): Serialized data.

    Returns:
    dict: A dictionary containing PyTorch tensors or NumPy arrays.
    """
    data = pickle.loads(serialized_data)
    if isinstance(data, dict):
        if 'torch_tensor' in data:
            data['torch_tensor'] = torch.tensor(data['torch_tensor'])
        if 'numpy_array' in data:
            data['numpy_array'] = np.array(data['numpy_array'])
    return data
