use pyo3::prelude::*;
use pyo3_tch::{wrap_tch_err, PyTensor};

#[pyfunction]
fn add_one(tensor: PyTensor) -> PyResult<PyTensor> {
    let tensor = tensor.f_add_scalar(1.0).map_err(wrap_tch_err)?;
    Ok(PyTensor(tensor))
}


#[pymodule]
#[pyo3(name = "torch_lib_with_rust")]
fn torch_mapping(py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    py.import_bound("torch")?;
    m.add_function(wrap_pyfunction!(add_one, m)?)?;

    Ok(())
}


