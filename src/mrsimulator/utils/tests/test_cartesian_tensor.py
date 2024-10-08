import numpy as np
import pytest
from mrsimulator.utils import cartesian_tensor as ct


def startup():
    tensor = np.array(
        [
            [-32.20646667, 19.7918, -13.8594],
            [-16.3634, -34.27226667, -0.2551],
            [7.5106, -0.1654, 66.47873333],
        ]
    )
    tensor_s = (tensor + tensor.T) / 2
    return tensor_s


def test_mehring():
    tensor_s = startup()
    euler_angle, eigenval = ct.to_mehring_params(tensor_s)

    assert np.allclose(eigenval, [66.58143614, -31.32167152, -35.25976463])

    tensor_out = ct.from_mehring_params(euler_angle, eigenval)

    assert np.allclose(tensor_s, tensor_out)


def test_haeberlen():
    tensor_s = startup()
    euler_angle, zeta, eta, iso = ct.to_haeberlen_params(tensor_s)

    assert np.allclose(zeta, 66.58143615)
    assert np.allclose(eta, 0.05914701)
    assert np.allclose(iso, 0)

    tensor_out = ct.from_haeberlen_params(euler_angle, zeta, eta, iso)

    assert np.allclose(tensor_s, tensor_out)

    sy_tensor = ct.to_symmetric_tensor(tensor_s, type="shielding")
    assert sy_tensor.D is None
    assert sy_tensor.Cq is None
    assert np.allclose(sy_tensor.zeta, zeta)
    assert np.allclose(sy_tensor.eta, eta)
    assert np.allclose(sy_tensor.alpha, euler_angle[0])
    assert np.allclose(sy_tensor.beta, euler_angle[1])
    assert np.allclose(sy_tensor.gamma, euler_angle[2])

    sy_tensor = ct.to_symmetric_tensor(tensor_s, type="quadrupolar")
    assert sy_tensor.zeta is None
    assert np.allclose(sy_tensor.Cq, zeta)

    with pytest.raises(ValueError, match="Unknown tensor type"):
        _ = ct.to_symmetric_tensor(tensor_s, type="acqua_man")


def test_generate_dipole():
    site1_coords = [2.1, 3.1, 1.3]  # coords for 1H in A
    site2_coords = [0, 0, 1.2]  # coords for 13C in A
    dipole_tensor = ct.dipolar_tensor(
        site_1=["1H", site1_coords], site_2=["13C", site2_coords]
    )

    ref_dipole_tensor = np.array(
        [
            [16.38990091, -400.118456, -12.90704697],
            [-400.118456, -303.21316686, -19.05325981],
            [-12.90704697, -19.05325981, 286.82326595],
        ]
    )

    assert np.allclose(dipole_tensor, ref_dipole_tensor)

    euler_angle, zeta, eta, iso = ct.to_haeberlen_params(dipole_tensor)
    assert np.allclose(iso, 0)

    sy_tensor = ct.to_symmetric_tensor(dipole_tensor, type="dipolar")
    assert sy_tensor.zeta is None
    assert sy_tensor.Cq is None
    assert np.allclose(sy_tensor.D, zeta)
    assert np.allclose(sy_tensor.eta, eta)
    assert np.allclose(sy_tensor.alpha, euler_angle[0])
    assert np.allclose(sy_tensor.beta, euler_angle[1])
    assert np.allclose(sy_tensor.gamma, euler_angle[2])

    # check dipolar coupling
    distance = np.linalg.norm(np.array(site1_coords) - np.array(site2_coords))
    dipolar_coupling = ct.dipolar_coupling_constant(
        isotope_symbol_1="1H",
        isotope_symbol_2="13C",
        distance=distance,
    )

    assert np.allclose(zeta, dipolar_coupling)


def test_mehring_maryland():
    principal_components = [66.58143614, -31.32167152, -35.25976463]
    span, skew, isotropic = ct.mehring_principal_components_to_maryland(
        principal_components
    )

    assert np.allclose(span, -101.84120077)
    assert np.allclose(skew, -0.92266208)
    assert np.allclose(isotropic, 0)

    lambdas = ct.maryland_to_mehring_principal_components(isotropic, span, skew)
    assert np.allclose(lambdas, principal_components)


def test_maryland_haeberlen():
    iso_in = 0
    skew = -0.92266208
    span = -101.84120077
    zeta, eta, iso_out = ct.maryland_to_haeberlen_params(iso_in, span, skew)

    assert np.allclose(zeta, 66.58143607)
    assert np.allclose(eta, 0.05914702)
    assert np.allclose(iso_out, 0)

    lambdas = ct.haeberlen_params_to_maryland(zeta, eta, iso_out)
    np.allclose(lambdas, [span, skew, iso_in])
