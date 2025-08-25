import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Switch } from './ui/switch';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Separator } from './ui/separator';
import { 
  User, 
  Bell, 
  Shield, 
  CreditCard, 
  Globe, 
  Users,
  Crown,
  Settings as SettingsIcon,
  Save,
  Key,
  Mail,
  Phone,
  Building
} from 'lucide-react';

export default function Settings() {
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem('user') || '{}'));
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);
  const token = localStorage.getItem('token');

  const isMasterAccount = user.role === 'master';

  const [profile, setProfile] = useState({
    firstName: user.first_name || '',
    lastName: user.last_name || '',
    email: user.email || '',
    agencyName: user.agency_name || '',
    phone: user.phone || '',
    bio: user.bio || ''
  });

  const [notifications, setNotifications] = useState({
    emailNotifications: true,
    smsNotifications: false,
    pushNotifications: true,
    weeklyReports: true,
    marketingEmails: false
  });

  const [integrations, setIntegrations] = useState({
    mailgun: { connected: true, status: 'Active' },
    stripe: { connected: true, status: 'Active' },
    twilio: { connected: true, status: 'Active' },
    openai: { connected: false, status: 'Temporarily Disabled' },
    facebook: { connected: false, status: 'Not Connected' },
    instagram: { connected: false, status: 'Not Connected' },
    linkedin: { connected: false, status: 'Not Connected' },
    twitter: { connected: false, status: 'Not Connected' }
  });

  const handleSaveProfile = async () => {
    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (error) {
      console.error('Save error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <SettingsIcon className="mr-3 h-8 w-8" />
            Settings
            {isMasterAccount && (
              <Badge variant="secondary" className="ml-3 bg-gold-100 text-gold-800 border-gold-300">
                <Crown className="w-3 h-3 mr-1" />
                Master Account
              </Badge>
            )}
          </h1>
          <p className="text-gray-600">Manage your account settings and preferences</p>
        </div>
        {saved && (
          <Badge variant="default" className="bg-green-100 text-green-800">
            <Save className="w-3 h-3 mr-1" />
            Settings Saved
          </Badge>
        )}
      </div>

      <Tabs defaultValue="profile" className="space-y-6">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="profile">Profile</TabsTrigger>
          <TabsTrigger value="account">Account</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
          <TabsTrigger value="integrations">Integrations</TabsTrigger>
          <TabsTrigger value="billing">Billing</TabsTrigger>
          <TabsTrigger value="security">Security</TabsTrigger>
        </TabsList>

        {/* Profile Settings */}
        <TabsContent value="profile" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <User className="mr-2 h-5 w-5" />
                Profile Information
              </CardTitle>
              <CardDescription>
                Update your profile information and business details
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="firstName">First Name</Label>
                  <Input
                    id="firstName"
                    value={profile.firstName}
                    onChange={(e) => setProfile({...profile, firstName: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="lastName">Last Name</Label>
                  <Input
                    id="lastName"
                    value={profile.lastName}
                    onChange={(e) => setProfile({...profile, lastName: e.target.value})}
                  />
                </div>
              </div>
              <div>
                <Label htmlFor="email">Email Address</Label>
                <Input
                  id="email"
                  type="email"
                  value={profile.email}
                  onChange={(e) => setProfile({...profile, email: e.target.value})}
                />
              </div>
              <div>
                <Label htmlFor="agencyName">Business/Agency Name</Label>
                <Input
                  id="agencyName"
                  value={profile.agencyName}
                  onChange={(e) => setProfile({...profile, agencyName: e.target.value})}
                />
              </div>
              <div>
                <Label htmlFor="phone">Phone Number</Label>
                <Input
                  id="phone"
                  type="tel"
                  value={profile.phone}
                  onChange={(e) => setProfile({...profile, phone: e.target.value})}
                />
              </div>
              <div>
                <Label htmlFor="bio">Bio</Label>
                <Textarea
                  id="bio"
                  placeholder="Tell us about yourself or your business..."
                  value={profile.bio}
                  onChange={(e) => setProfile({...profile, bio: e.target.value})}
                />
              </div>
              <Button onClick={handleSaveProfile} disabled={loading}>
                {loading ? 'Saving...' : 'Save Profile'}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Account Settings */}
        <TabsContent value="account" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Account Status</CardTitle>
              <CardDescription>Your current account information and limits</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <Label>Account Type</Label>
                    <div className="flex items-center mt-1">
                      {isMasterAccount ? (
                        <Badge className="bg-gradient-to-r from-yellow-400 to-yellow-600">
                          <Crown className="w-3 h-3 mr-1" />
                          Master Account
                        </Badge>
                      ) : (
                        <Badge variant="secondary">Standard Account</Badge>
                      )}
                    </div>
                  </div>
                  <div>
                    <Label>Subscription Status</Label>
                    <p className="text-sm text-gray-600 mt-1">
                      {isMasterAccount ? 'Unlimited Access' : user.subscription_status || 'Trial'}
                    </p>
                  </div>
                  <div>
                    <Label>Member Since</Label>
                    <p className="text-sm text-gray-600 mt-1">
                      {user.created_at ? new Date(user.created_at).toLocaleDateString() : 'Recently joined'}
                    </p>
                  </div>
                </div>
                <div className="space-y-4">
                  <div>
                    <Label>Account Limits</Label>
                    <div className="mt-2 space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Websites</span>
                        <span>{isMasterAccount ? 'Unlimited' : '10'}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Sub-Accounts</span>
                        <span>{isMasterAccount ? 'Unlimited' : '5'}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>AI Content Generation</span>
                        <span>{isMasterAccount ? 'Unlimited' : '100/month'}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Custom Domains</span>
                        <span>{isMasterAccount ? 'Unlimited' : '3'}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {isMasterAccount && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Users className="mr-2 h-5 w-5" />
                  Master Account Features
                </CardTitle>
                <CardDescription>
                  Advanced features available to master accounts
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <span className="font-medium">White-Label Solutions</span>
                    <Badge className="bg-green-100 text-green-800">Active</Badge>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <span className="font-medium">Reseller Program</span>
                    <Badge className="bg-green-100 text-green-800">Active</Badge>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <span className="font-medium">Priority Support</span>
                    <Badge className="bg-green-100 text-green-800">Active</Badge>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <span className="font-medium">Custom Branding</span>
                    <Badge className="bg-green-100 text-green-800">Active</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Notification Settings */}
        <TabsContent value="notifications" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Bell className="mr-2 h-5 w-5" />
                Notification Preferences
              </CardTitle>
              <CardDescription>
                Choose how you want to receive notifications
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {Object.entries(notifications).map(([key, value]) => (
                <div key={key} className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label className="font-medium">
                      {key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                    </Label>
                    <p className="text-sm text-gray-500">
                      {key === 'emailNotifications' && 'Receive notifications via email'}
                      {key === 'smsNotifications' && 'Receive notifications via SMS'}
                      {key === 'pushNotifications' && 'Receive push notifications in browser'}
                      {key === 'weeklyReports' && 'Receive weekly performance reports'}
                      {key === 'marketingEmails' && 'Receive marketing and promotional emails'}
                    </p>
                  </div>
                  <Switch
                    checked={value}
                    onCheckedChange={(checked) => 
                      setNotifications({...notifications, [key]: checked})
                    }
                  />
                </div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Integrations */}
        <TabsContent value="integrations" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Service Integrations</CardTitle>
              <CardDescription>
                Manage your connected services and APIs
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(integrations).map(([service, details]) => (
                  <div key={service} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                        {service === 'mailgun' && <Mail className="w-5 h-5" />}
                        {service === 'stripe' && <CreditCard className="w-5 h-5" />}
                        {service === 'twilio' && <Phone className="w-5 h-5" />}
                        {service === 'openai' && <Shield className="w-5 h-5" />}
                        {['facebook', 'instagram', 'linkedin', 'twitter'].includes(service) && <Globe className="w-5 h-5" />}
                      </div>
                      <div>
                        <h4 className="font-medium capitalize">{service}</h4>
                        <p className="text-sm text-gray-500">{details.status}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge variant={details.connected ? 'default' : 'secondary'}>
                        {details.connected ? 'Connected' : 'Not Connected'}
                      </Badge>
                      <Button variant="outline" size="sm">
                        {details.connected ? 'Configure' : 'Connect'}
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Billing */}
        <TabsContent value="billing" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <CreditCard className="mr-2 h-5 w-5" />
                Billing & Subscription
              </CardTitle>
              <CardDescription>
                Manage your billing information and subscription
              </CardDescription>
            </CardHeader>
            <CardContent>
              {isMasterAccount ? (
                <div className="text-center py-8">
                  <Crown className="w-16 h-16 mx-auto text-yellow-600 mb-4" />
                  <h3 className="text-xl font-semibold mb-2">Master Account</h3>
                  <p className="text-gray-600 mb-4">
                    You have unlimited access to all features. No billing required.
                  </p>
                  <Button>Manage Sub-Account Billing</Button>
                </div>
              ) : (
                <div className="space-y-4">
                  <div>
                    <Label>Current Plan</Label>
                    <p className="text-lg font-semibold">Free Trial</p>
                    <p className="text-sm text-gray-500">
                      {user.days_remaining || 30} days remaining
                    </p>
                  </div>
                  <Separator />
                  <div>
                    <h4 className="font-medium mb-2">Upgrade Options</h4>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="border rounded-lg p-4">
                        <h5 className="font-semibold">Professional</h5>
                        <p className="text-2xl font-bold">$29/mo</p>
                        <p className="text-sm text-gray-500">Perfect for small businesses</p>
                        <Button className="w-full mt-2">Choose Plan</Button>
                      </div>
                      <div className="border rounded-lg p-4">
                        <h5 className="font-semibold">Business</h5>
                        <p className="text-2xl font-bold">$79/mo</p>
                        <p className="text-sm text-gray-500">Great for growing companies</p>
                        <Button className="w-full mt-2">Choose Plan</Button>
                      </div>
                      <div className="border rounded-lg p-4">
                        <h5 className="font-semibold">Enterprise</h5>
                        <p className="text-2xl font-bold">$199/mo</p>
                        <p className="text-sm text-gray-500">Full-featured solution</p>
                        <Button className="w-full mt-2">Choose Plan</Button>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Security */}
        <TabsContent value="security" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Shield className="mr-2 h-5 w-5" />
                Security Settings
              </CardTitle>
              <CardDescription>
                Manage your account security and privacy settings
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <h4 className="font-medium mb-4">Change Password</h4>
                <div className="space-y-4 max-w-md">
                  <div>
                    <Label htmlFor="currentPassword">Current Password</Label>
                    <Input id="currentPassword" type="password" />
                  </div>
                  <div>
                    <Label htmlFor="newPassword">New Password</Label>
                    <Input id="newPassword" type="password" />
                  </div>
                  <div>
                    <Label htmlFor="confirmPassword">Confirm New Password</Label>
                    <Input id="confirmPassword" type="password" />
                  </div>
                  <Button>Update Password</Button>
                </div>
              </div>
              <Separator />
              <div>
                <h4 className="font-medium mb-4">API Keys</h4>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-medium">API Key</p>
                      <p className="text-sm text-gray-500">Access your account programmatically</p>
                    </div>
                    <Button variant="outline" size="sm">
                      <Key className="w-4 h-4 mr-1" />
                      Generate
                    </Button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}