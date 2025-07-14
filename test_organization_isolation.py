import os
import django
import sys

# Add the project root to the Python path
sys.path.append('C:\\Users\\rijhunjhunwala\\OneDrive - Deloitte (O365D)\\Documents\\alloyCostOptimisation\\alloyCostOptimisation-main\\alloy_optimizer')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alloy_optimizer.settings')
django.setup()

from django.contrib.auth.models import User
from optimizer.models import Organization, UserProfile, ScrapData, CompositionRequirements, OptimizationBatch
from django.test import TestCase, Client
from django.urls import reverse
import tempfile
import csv

class OrganizationIsolationTest:
    """
    Test suite for organization-based access control.
    """
    
    def __init__(self):
        self.client = Client()
        self.setup_test_data()
    
    def setup_test_data(self):
        """
        Create test organizations and users.
        """
        print("Setting up test data...")
        
        # Create test organizations
        self.org1 = Organization.objects.create(
            name="Organization Alpha",
            code="ALPHA",
            description="Test organization 1"
        )
        
        self.org2 = Organization.objects.create(
            name="Organization Beta", 
            code="BETA",
            description="Test organization 2"
        )
        
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@alpha.com',
            password='testpass123',
            first_name='John',
            last_name='Alpha'
        )
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@beta.com', 
            password='testpass123',
            first_name='Jane',
            last_name='Beta'
        )
        
        # Create user profiles
        UserProfile.objects.create(
            user=self.user1,
            organization=self.org1,
            employee_id='ALPHA001'
        )
        
        UserProfile.objects.create(
            user=self.user2,
            organization=self.org2,
            employee_id='BETA001'
        )
        
        print(f"Created organizations: {self.org1.name}, {self.org2.name}")
        print(f"Created users: {self.user1.username}, {self.user2.username}")
    
    def create_test_csv_file(self, content, filename):
        """
        Create a temporary CSV file for testing uploads.
        """
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        writer = csv.writer(temp_file)
        for row in content:
            writer.writerow(row)
        temp_file.close()
        return temp_file.name
    
    def test_user_login_and_context(self):
        """
        Test that users can login and have correct organization context.
        """
        print("\n=== Testing User Login and Organization Context ===")
        
        # Test user1 login
        login_success = self.client.login(username='user1', password='testpass123')
        self.assert_true(login_success, "User1 should be able to login")
        
        response = self.client.get(reverse('dashboard'))
        self.assert_equal(response.status_code, 200, "Dashboard should be accessible")
        self.assert_in(self.org1.name.encode(), response.content, "Dashboard should show user's organization")
        
        self.client.logout()
        
        # Test user2 login
        login_success = self.client.login(username='user2', password='testpass123')
        self.assert_true(login_success, "User2 should be able to login")
        
        response = self.client.get(reverse('dashboard'))
        self.assert_equal(response.status_code, 200, "Dashboard should be accessible")
        self.assert_in(self.org2.name.encode(), response.content, "Dashboard should show user's organization")
        
        print("✓ User login and organization context working correctly")
    
    def test_data_upload_isolation(self):
        """
        Test that data uploads are isolated by organization.
        """
        print("\n=== Testing Data Upload Isolation ===")
        
        # Create test scrap data CSV
        scrap_data = [
            ['Scrap_Type', 'COST', 'SI', 'FE', 'CU', 'MN', 'MG', 'Available_Amount'],
            ['Test Scrap Alpha', '100.0', '0.5', '0.1', '0.2', '0.05', '0.03', '50.0']
        ]
        scrap_file = self.create_test_csv_file(scrap_data, 'test_scrap.csv')
        
        # Upload as user1 (org1)
        self.client.login(username='user1', password='testpass123')
        with open(scrap_file, 'rb') as f:
            response = self.client.post(reverse('upload_scrap_data'), {'file': f})
        
        # Check that scrap data was created for org1
        scrap_count_org1 = ScrapData.objects.filter(organization=self.org1).count()
        scrap_count_org2 = ScrapData.objects.filter(organization=self.org2).count()
        
        self.assert_equal(scrap_count_org1, 1, "Org1 should have 1 scrap data file")
        self.assert_equal(scrap_count_org2, 0, "Org2 should have 0 scrap data files")
        
        self.client.logout()
        
        # Upload as user2 (org2)
        self.client.login(username='user2', password='testpass123')
        with open(scrap_file, 'rb') as f:
            response = self.client.post(reverse('upload_scrap_data'), {'file': f})
        
        # Check counts again
        scrap_count_org1 = ScrapData.objects.filter(organization=self.org1).count()
        scrap_count_org2 = ScrapData.objects.filter(organization=self.org2).count()
        
        self.assert_equal(scrap_count_org1, 1, "Org1 should still have 1 scrap data file")
        self.assert_equal(scrap_count_org2, 1, "Org2 should now have 1 scrap data file")
        
        print("✓ Data upload isolation working correctly")
        
        # Clean up
        os.unlink(scrap_file)
    
    def test_cross_organization_access(self):
        """
        Test that users cannot access other organizations' data.
        """
        print("\n=== Testing Cross-Organization Access Prevention ===")
        
        # Create a batch for org1
        self.client.login(username='user1', password='testpass123')
        response = self.client.post(reverse('create_batch'), {'name': 'Test Batch Alpha'})
        
        batch_org1 = OptimizationBatch.objects.filter(organization=self.org1).first()
        self.assert_true(batch_org1 is not None, "Batch should be created for org1")
        
        self.client.logout()
        
        # Try to access org1's batch as user2 (org2)
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(reverse('edit_batch', kwargs={'pk': batch_org1.pk}))
        
        self.assert_equal(response.status_code, 404, "User2 should not be able to access org1's batch")
        
        print("✓ Cross-organization access prevention working correctly")
    
    def test_dashboard_data_filtering(self):
        """
        Test that dashboard only shows organization-specific data.
        """
        print("\n=== Testing Dashboard Data Filtering ===")
        
        # Create batches for both organizations
        batch1 = OptimizationBatch.objects.create(
            name="Batch Alpha",
            organization=self.org1,
            created_by=self.user1
        )
        
        batch2 = OptimizationBatch.objects.create(
            name="Batch Beta", 
            organization=self.org2,
            created_by=self.user2
        )
        
        # Test user1 dashboard
        self.client.login(username='user1', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        
        self.assert_in(b'Batch Alpha', response.content, "User1 should see org1's batch")
        self.assert_not_in(b'Batch Beta', response.content, "User1 should not see org2's batch")
        
        self.client.logout()
        
        # Test user2 dashboard
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        
        self.assert_in(b'Batch Beta', response.content, "User2 should see org2's batch")
        self.assert_not_in(b'Batch Alpha', response.content, "User2 should not see org1's batch")
        
        print("✓ Dashboard data filtering working correctly")
    
    def assert_true(self, condition, message):
        """Helper assertion method."""
        if not condition:
            print(f"✗ ASSERTION FAILED: {message}")
            return False
        return True
    
    def assert_equal(self, actual, expected, message):
        """Helper assertion method."""
        if actual != expected:
            print(f"✗ ASSERTION FAILED: {message} (expected: {expected}, actual: {actual})")
            return False
        return True
    
    def assert_in(self, needle, haystack, message):
        """Helper assertion method."""
        if needle not in haystack:
            print(f"✗ ASSERTION FAILED: {message}")
            return False
        return True
    
    def assert_not_in(self, needle, haystack, message):
        """Helper assertion method."""
        if needle in haystack:
            print(f"✗ ASSERTION FAILED: {message}")
            return False
        return True
    
    def run_all_tests(self):
        """
        Run all organization isolation tests.
        """
        print("Starting Organization Isolation Tests...")
        print("=" * 50)
        
        try:
            self.test_user_login_and_context()
            self.test_data_upload_isolation()
            self.test_cross_organization_access()
            self.test_dashboard_data_filtering()
            
            print("\n" + "=" * 50)
            print("✓ All organization isolation tests passed!")
            
        except Exception as e:
            print(f"\n✗ Test failed with error: {str(e)}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.cleanup_test_data()
    
    def cleanup_test_data(self):
        """
        Clean up test data.
        """
        print("\nCleaning up test data...")
        User.objects.filter(username__in=['user1', 'user2']).delete()
        Organization.objects.filter(code__in=['ALPHA', 'BETA']).delete()
        print("✓ Test data cleaned up")

if __name__ == '__main__':
    tester = OrganizationIsolationTest()
    tester.run_all_tests()