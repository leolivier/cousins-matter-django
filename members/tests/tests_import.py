from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import translation
# from django.utils.translation import gettext as _
from datetime import date
from ..models import ALL_FIELD_NAMES, MANDATORY_FIELD_NAMES, Member
from .tests_member import MemberTestCase
from ..views.views_import import CSVImportView
import os


def get_test_file(filename):
  return os.path.join(os.path.dirname(__file__), 'resources', filename)


class TestMemberImport(MemberTestCase):

  def test_get_import(self):
    response = self.client.get(reverse('members:csv_import'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'members/import_members.html')
    self.assertIs(response.resolver_match.func.view_class, CSVImportView)

  def do_upload_file(self, file, lang, activate_users=True):
    url = reverse('members:csv_import')
    csv_file = get_test_file(file)
    # force language to make sure the CSV fields are ok
    with translation.override(lang):
      response = self.client.post(url,
                                  {'csv_file': SimpleUploadedFile(file,
                                                                  open(csv_file, 'rb').read(),
                                                                  content_type='text/csv'),
                                    'activate_users': activate_users
                                   }, follow=True)
    # print(response.content)
    return response

  def do_test_import(self, file, lang, expected_num, activate_users=True):
    prev_num = Member.objects.count()
    response = self.do_upload_file(file, lang)
    self.assertEqual(response.status_code, 200)
    # Check that expected_num members were imported
    self.assertEqual(Member.objects.count(), prev_num+expected_num)
    # Check that specific members were created
    self.assertTrue(Member.objects.filter(account__first_name='John', account__last_name='Doe').exists())
    self.assertTrue(Member.objects.filter(account__email='member2@test.com').exists())
    self.assertTrue(Member.objects.filter(address__city='Blackpool').exists())
    self.assertTrue(Member.objects.filter(birthdate=date(2000, 1, 3)).exists())
    for name in ['member1', 'member2', 'member3', 'member4']:
      m = Member.objects.get(account__username=name)
      if activate_users:
        self.assertEqual(m.account.is_active, activate_users)
        self.assertEqual(m.account, m.managing_account)
      else:  # account=managing_account if and only if active
        self.assertEqual(m.account == m.managing_account, m.account.is_active)

  def test_import_en(self):
    """test the import in english (create and update)"""
    # more or less the same as 1rst line of import file with differences on first_name, birthdate and phone
    data = {'username': "member1", 'email': "member1@test.com", 'password1': self.password, 'password2': self.password,
            'first_name': "Johnny", 'last_name': "Doe", 'birhdtate': date(2001, 1, 1), 'phone': "+45 01 02 30"}
    member1 = self.create_member(data)
    self.do_test_import('import_members.csv', 'en-US', 3)  # expected 3 and not 4 because we just created one above
    member1.refresh_from_db()
    # check the changes have been taken from the import file
    self.assertEqual(member1.first_name(), "John")
    self.assertEqual(member1.birthdate, date(2000, 1, 1))
    self.assertEqual(member1.phone, "+45 01 02 03")

  def test_import_fr(self):
    self.do_test_import('import_members-fr.csv', 'fr-FR', 4)

  def test_wrong_field(self):
    response = self.do_upload_file('import_members-wrong-field.csv', 'en-US')
    self.assertEqual(response.status_code, 200)
    self.assertContainsMessage(
      response, "error",
      'Unknown column in CSV file: "%(fieldname)s". Valid fields are %(all_names)s' % {
        'fieldname': "citi",
        'all_names': ", ".join(ALL_FIELD_NAMES.keys())
      })

  def test_missing_field(self):
    response = self.do_upload_file('import_members-missing-field.csv', 'en-US')
    self.assertEqual(response.status_code, 200)
    self.assertContainsMessage(response, "error",
                               'Missing column in CSV file: \"%(fieldname)s\". Mandatory fields are %(all_names)s' % {
                                   'fieldname': "first_name",
                                   'all_names': ", ".join([str(s) for s in MANDATORY_FIELD_NAMES.keys()])
                               })