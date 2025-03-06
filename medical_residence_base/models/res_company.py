from odoo import fields, models, api , _


class Company(models.Model):
    _inherit="res.company"
    
    
    def action_create_dms_structure(self):
        company_storage = self._create_dms_storage()
        self._create_root_dirs(company_storage)
    
    
    def _create_xml_id(self, **kw):
        self.env['ir.model.data'].create(kw)
        
        
    def _create_root_dirs(self, storage):
        for dir_name, dir_key in (
            (_('Residents'), 'residents'), 
            (_('Employees'), 'employees')
            ):
            
            directory = self.env.ref(
            'medical_residence_base.dms_%s_%s' % (dir_key ,self.id),
            raise_if_not_found=False
            )
            
            if directory:
                if directory.storage_id.id != storage.id:
                    directory_storage_id = storage.id
                continue
                
            directory = self.env['dms.directory'].create({
                'name': dir_name,
                'is_root_directory': True,
                'color': 1,
                'storage_id' : storage.id,
                'category_id' : self.env.ref('medical_residence_base.documents_%s_documents' % dir_key).id,
                'group_ids': [(6,0,[
                    self.env.ref('medical_residence_base.access_group_dms_admin').id,
                    self.env.ref('medical_residence_base.access_group_dms_employees').id
                ])]  
            })
            self._create_xml_id(
                module='medical_residence_base',
                name="dms_%s_%s" % (dir_key,self.id), 
                model='dms.directory',
                res_id=directory.id,
                noupdate=True
            )
    
    def _create_dms_storage(self):
        Storage = self.env['dms.storage']
        company_storage = self.env.ref(
            'medical_residence_base.dms_storage_%s' % self.id,
            raise_if_not_found=False
        )
        if company_storage:
            return company_storage
        company_storage = Storage.create({
            'name' : self.name,
            'save_type' : 'database', 
            'company_id': self.id
        })
        self._create_xml_id(
            module='medical_residence_base',
            name="dms_storage_%s" % self.id, 
            model='dms.storage',
            res_id=company_storage.id,
            noupdate=True
            )
        return company_storage