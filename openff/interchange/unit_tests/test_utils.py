import numpy as np
from openff.toolkit.typing.engines.smirnoff import ForceField
from openff.units import unit
from openff.units.openmm import from_openmm
from openmm import unit as openmm_unit

from openff.interchange.testing import _BaseTest
from openff.interchange.utils import (
    _unwrap_list_of_pint_quantities,
    compare_forcefields,
    get_partial_charges_from_openmm_system,
    pint_to_openmm,
)

openmm_quantitites = [
    4.0 * openmm_unit.nanometer,
    5.0 * openmm_unit.angstrom,
    1.0 * openmm_unit.elementary_charge,
]

pint_quantities = [
    4.0 * unit.nanometer,
    5.0 * unit.angstrom,
    1.0 * unit.elementary_charge,
]


def test_openmm_list_of_quantities_to_pint():
    """Test conversion from Quantity lists, lists of Quantity"""
    list_of_quantities = [val * openmm_unit.meter for val in range(10)]
    quantity_list = openmm_unit.meter * [val for val in range(10)]

    assert list_of_quantities != quantity_list
    assert all(from_openmm(list_of_quantities) == from_openmm(quantity_list))


def test_pint_to_openmm():
    """Test conversion from pint Quantity to SimTK Quantity."""
    q = 5.0 / unit.nanometer
    assert pint_to_openmm(q) == 0.5 / openmm_unit.angstrom


class TestUtils(_BaseTest):
    def test_compare_forcefields(self, parsley):
        parsley_name = "openff-1.0.0.offxml"
        compare_forcefields(parsley, parsley)
        compare_forcefields(ForceField(parsley_name), parsley)
        compare_forcefields(parsley, ForceField(parsley_name))
        compare_forcefields(ForceField(parsley_name), ForceField(parsley_name))

    def test_unwrap_quantities(self):
        wrapped = [1 * unit.m, 1.5 * unit.m]
        unwrapped = [1, 1.5] * unit.m

        assert all(unwrapped == _unwrap_list_of_pint_quantities(wrapped))


class TestOpenMM(_BaseTest):
    def test_openmm_partial_charges(self, argon_ff, argon_top):
        omm_system = argon_ff.create_openmm_system(argon_top)
        partial_charges = get_partial_charges_from_openmm_system(omm_system)

        # assert isinstance(partial_charges, unit.Quantity)
        # assert partial_charges.units == unit.elementary_charge
        assert isinstance(partial_charges, list)
        assert np.allclose(partial_charges, np.zeros(4))  # .magnitude
