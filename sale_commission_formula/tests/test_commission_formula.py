# -*- coding: utf-8 -*-
# © 2016 Nicola Malcontenti - Agile Business Group
# © 2016 Davide Corio - Abstract
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests.common import TransactionCase


class TestCommissionFormula(TransactionCase):

    def setUp(self):
        super(TestCommissionFormula, self).setUp()
        self.agent = self.env.ref('sale_commission_formula.agent1')
        self.agent2 = self.env.ref('sale_commission_formula.agent2')
        self.commission = self.env.ref(
            'sale_commission_formula.commission_5perc10extra')
        self.commission2 = self.env.ref('sale_commission_formula.commission_alwaysplus10')
        self.sale_order = self.env.ref('sale_commission_formula.sale_order_1')
        self.sale_order2 = self.env.ref('sale_commission_formula.sale_order_2')
        self.sale_order_line = self.env.ref(
            'sale_commission_formula.sale_order_line_1')
        self.sale_order_line2 = self.env.ref(
            'sale_commission_formula.sale_order_line_2')
        self.agent_commissions = {
            'agent': self.agent.id, 'commission': self.commission.id}
        self.agent_commissions2 = {
            'agent': self.agent.id, 'commission': self.commission2.id}

    def test_sale_order_commission(self):
        # we test the '5% + 10% extra' we should return 41.25 since
        # the order total amount is 750.00.
        self.sale_order_line.agents = [(0, 0, self.agent_commissions)]
        self.assertEqual(41.25, self.sale_order.commission_total)

    def test_sale_order_commission_2(self):
        """
        Test applying 2 commissions for the same agent for the total of 750
        - 5% + 10% extra is 41.25
        - +10$
        """
        self.sale_order_line2.agents = [
            (0, 0, self.agent_commissions),
            (0, 0, self.agent_commissions2),
        ]
        self.assertEqual(51.25, self.sale_order2.commission_total)

    def test_invoice_commission2(self):
        # we confirm the sale order and create the corresponding invoice
        self.sale_order2.action_button_confirm()
        invoice_id = self.sale_order2.action_invoice_create()
        invoice = self.env['account.invoice'].browse(invoice_id)
        # we add the commissions on the first invoice line
        invoice_line = invoice.invoice_line[0]
        invoice_line.agents = [
            (0, 0, self.agent_commissions),
            (0, 0, self.agent_commissions2),
        ]
        # we test the '5% + 10% extra' commissions on the invoice too + 10 (second commission)
        self.assertEqual(51.25, invoice.commission_total)

    def test_invoice_commission(self):
        # we confirm the sale order and create the corresponding invoice
        self.sale_order.action_button_confirm()
        invoice_id = self.sale_order.action_invoice_create()
        invoice = self.env['account.invoice'].browse(invoice_id)
        # we add the commissions on the first invoice line
        invoice_line = invoice.invoice_line[0]
        invoice_line.agents = [(0, 0, self.agent_commissions)]
        # we test the '5% + 10% extra' commissions on the invoice too
        self.assertEqual(41.25, invoice.commission_total)
