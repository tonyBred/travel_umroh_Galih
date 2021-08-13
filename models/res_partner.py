from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date, timedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'

    no_ktp = fields.Char(string='KTP No')
    gender = fields.Selection([("male","Male"),("female","Female")], string='Gender')
    father_name = fields.Char(string="""Father's Name""")
    mother_name = fields.Char(string="""Mother's Name""")
    job = fields.Char(string='Job')
    place_birth = fields.Char(string='Place of Birth')
    date_birth = fields.Date(string='Date of Birth')
    blood_type = fields.Selection([("a","A"),("b","B"),("ab","AB"),("o","O")], string='Blood Type')
    martial_status = fields.Selection([("married","Married"),("not","Not Married"),("divorce","Divorce")], string='Martial Status')
    education = fields.Selection([("sd","SD"),("smp","SMP"),("sma","SMA/SMK"),("diploma","Diploma"),("sarjana","Sarjana")], string='Education')
    mahram = fields.Many2one(
        comodel_name='res.partner',
        string='Mahram',
        domain=[("martial_status", "=", "married")],
    )
    age = fields.Integer(
        string='Umur',
        compute='_compute_age',
        store=False,
        )
    
    @api.depends('date_birth')
    def _compute_age(self):
        for o in self:
            o.age = False
            if o.date_birth == date.today():
                o.age = 0
            elif o.date_birth:
                delta = date.today() - o.date_birth
                o.age = delta.days / 365
            