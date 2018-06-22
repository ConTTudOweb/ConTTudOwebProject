from django.urls import reverse

from ..admin import admin


class ModelAdminTest:
    ModelAdmin = None
    Model = None
    readonly_fields = ()
    exclude = None

    def setUp(self):
        if self.ModelAdmin is None:
            raise NotImplementedError("'ModelAdmin' não implementado!")
        if self.Model is None:
            raise NotImplementedError("'Model' não implementado!")

        self.model_admin = self.ModelAdmin(self.Model, admin.site)

    def test_search_fields(self):
        self.assertNotEqual(self.model_admin.search_fields, ())

    def test_list_display(self):
        self.assertNotEqual(self.model_admin.list_display, ('__str__',))

    def test_readonly_fields(self):
        self.assertEqual(self.model_admin.readonly_fields, self.readonly_fields)

    def test_exclude_fields(self):
        self.assertEqual(self.model_admin.exclude, self.exclude)

    def test_has_url_in_admin(self):
        self.Model._meta.app_label
        self.assertNotEqual(reverse('admin:' +
                                    self.Model._meta.app_label + '_' +
                                    self.Model._meta.model_name + '_changelist'), '')

    class Meta:
        abstract = True
