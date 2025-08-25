import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { 
  Users, 
  DollarSign, 
  TrendingUp, 
  Activity,
  ArrowUpRight,
  ArrowDownRight,
  Plus,
  Globe,
  Zap,
  BarChart,
  MessageCircle,
  ShoppingCart,
  Crown
} from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

// Sample data for charts
const revenueData = [
  { month: 'Jan', revenue: 12000, leads: 45 },
  { month: 'Feb', revenue: 15000, leads: 52 },
  { month: 'Mar', revenue: 18000, leads: 61 },
  { month: 'Apr', revenue: 22000, leads: 73 },
  { month: 'May', revenue: 25000, leads: 84 },
  { month: 'Jun', revenue: 28000, leads: 92 },
];

const recentActivities = [
  { id: 1, type: 'contact', message: 'New contact Sarah Johnson added', time: '2 minutes ago' },
  { id: 2, type: 'deal', message: 'Deal with TechCorp moved to negotiation', time: '15 minutes ago' },
  { id: 3, type: 'email', message: 'Email campaign "Summer Sale" sent to 1,250 contacts', time: '1 hour ago' },
  { id: 4, type: 'meeting', message: 'Meeting scheduled with Digital Marketing Pro', time: '2 hours ago' },
];

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const token = localStorage.getItem('token');
  
  // Fetch comprehensive dashboard data from backend
  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/dashboard`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          setDashboardData(data);
        } else {
          setError('Failed to load dashboard data');
        }
      } catch (err) {
        setError('Network error loading dashboard');
        console.error('Dashboard fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchDashboard();
    }
  }, [token]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your business platform...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="text-red-500 mb-4">
            <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 18.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Loading Error</h3>
          <p className="text-red-600 mb-4">{error}</p>
          <Button onClick={() => window.location.reload()} className="bg-blue-600 hover:bg-blue-700">
            Retry Loading
          </Button>
        </div>
      </div>
    );
  }

  const isMasterAccount = dashboardData?.account_type === 'Master Account';
  const isWhiteLabelAccount = dashboardData?.account_type === 'White Label Partner';
  const isTrialUser = !isMasterAccount && !isWhiteLabelAccount && (dashboardData?.subscription_info?.is_trial || user.subscription_status === 'trial');
  const stats = dashboardData?.quick_stats || {
    total_contacts: 0,
    total_websites: 0,
    total_funnels: 0,
    total_content_pieces: 0,
    active_automations: 0,
    monthly_revenue: 0
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center space-x-3">
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            {isMasterAccount && (
              <Badge variant="secondary" className="bg-gold-100 text-gold-800 border-gold-300">
                <Crown className="w-3 h-3 mr-1" />
                Master Account
              </Badge>
            )}
          </div>
          <p className="text-gray-600">
            Welcome back, {dashboardData?.user?.first_name || user.name || 'User'}! 
            {isMasterAccount && ' You have unlimited access to all platform features.'}
          </p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Add Contact
        </Button>
      </div>

      {/* Account Status Banner */}
      {isMasterAccount ? (
        <Card className="border-green-200 bg-gradient-to-r from-green-50 to-blue-50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-green-900 flex items-center">
                  <Crown className="w-5 h-5 mr-2 text-yellow-600" />
                  Master Account - Unlimited Access
                </h3>
                <p className="text-green-700">
                  You have full access to all business platform features including white-label solutions, 
                  unlimited websites, AI content creation, and reseller capabilities.
                </p>
              </div>
              <Button className="bg-blue-600 hover:bg-blue-700">
                Manage Sub-Accounts
              </Button>
            </div>
          </CardContent>
        </Card>
      ) : isWhiteLabelAccount ? (
        <Card className="border-purple-200 bg-gradient-to-r from-purple-50 to-blue-50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-purple-900 flex items-center">
                  <Crown className="w-5 h-5 mr-2 text-purple-600" />
                  White Label Partner - Reseller Access
                </h3>
                <p className="text-purple-700">
                  Complete white-label solution with unlimited capabilities. Create sub-accounts, 
                  custom branding, and earn revenue through our reseller program.
                </p>
              </div>
              <Button className="bg-purple-600 hover:bg-purple-700">
                Manage Branding
              </Button>
            </div>
          </CardContent>
        </Card>
      ) : isTrialUser ? (
        <Card className="border-blue-200 bg-blue-50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-blue-900">Free Trial Active</h3>
                <p className="text-blue-700">
                  You have {dashboardData?.subscription_info?.days_remaining || dashboardData?.user?.days_remaining || 30} days left in your trial. Upgrade now to unlock all features!
                </p>
              </div>
              <Button className="bg-blue-600 hover:bg-blue-700">
                Upgrade Now
              </Button>
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card className="border-green-200 bg-green-50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-green-900">
                  {dashboardData?.account_type || 'Active Plan'}
                </h3>
                <p className="text-green-700">
                  Your subscription is active. Enjoy all the features available in your plan.
                </p>
              </div>
              <Button className="bg-green-600 hover:bg-green-700">
                View Plan Details
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Comprehensive Business Platform Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 xl:grid-cols-6 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Contacts</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_contacts || 0}</div>
            <p className="text-xs text-muted-foreground">
              {(isMasterAccount || isWhiteLabelAccount) ? 'Unlimited' : 'Trial limit: 100'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Websites</CardTitle>
            <Globe className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_websites || 0}</div>
            <p className="text-xs text-muted-foreground">
              {(isMasterAccount || isWhiteLabelAccount) ? 'Unlimited' : 'Trial limit: 3'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Funnels</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_funnels || 0}</div>
            <p className="text-xs text-muted-foreground">
              {(isMasterAccount || isWhiteLabelAccount) ? 'Unlimited' : 'Trial limit: 5'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Content</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total_content_pieces || 0}</div>
            <p className="text-xs text-muted-foreground">
              AI-generated pieces
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Automations</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.active_automations || 0}</div>
            <p className="text-xs text-muted-foreground">
              Active workflows
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${stats.monthly_revenue || 0}</div>
            <p className="text-xs text-muted-foreground">
              This month
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Business Platform Features */}
      <Card>
        <CardHeader>
          <CardTitle>Ultimate Business Platform Features</CardTitle>
          <CardDescription>Your all-in-one business solution - everything you need in one place</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
            {(dashboardData?.available_features || []).map((feature, index) => (
              <Card key={index} className={`cursor-pointer transition-all hover:shadow-md ${
                feature.enabled ? 'border-green-200 bg-green-50' : 'border-gray-200 bg-gray-50'
              }`}>
                <CardContent className="p-4">
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg ${
                      feature.enabled ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-400'
                    }`}>
                      {feature.icon === 'globe' && <Globe className="w-5 h-5" />}
                      {feature.icon === 'users' && <Users className="w-5 h-5" />}
                      {feature.icon === 'edit' && <Activity className="w-5 h-5" />}
                      {feature.icon === 'trending-up' && <TrendingUp className="w-5 h-5" />}
                      {feature.icon === 'user-check' && <Users className="w-5 h-5" />}
                      {feature.icon === 'shopping-cart' && <ShoppingCart className="w-5 h-5" />}
                      {feature.icon === 'zap' && <Zap className="w-5 h-5" />}
                      {feature.icon === 'bar-chart' && <BarChart className="w-5 h-5" />}
                      {feature.icon === 'message-circle' && <MessageCircle className="w-5 h-5" />}
                      {feature.icon === 'clipboard' && <Activity className="w-5 h-5" />}
                    </div>
                    <div className="flex-1">
                      <h4 className="font-semibold text-sm">{feature.name}</h4>
                      <p className="text-xs text-gray-600">{feature.description}</p>
                      {feature.enabled && (
                        <Badge variant="secondary" className="mt-1 text-xs">
                          Active
                        </Badge>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Charts and Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
            <CardDescription>Latest updates from your business platform</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {(dashboardData?.recent_activity || []).map((activity, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">{activity.description}</p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              )) || [
                { description: 'Welcome to Brainstorm AI Kit!', time: 'Just now' },
                { description: 'Your comprehensive business platform is ready', time: '1 minute ago' },
                { description: 'All features have been activated', time: '2 minutes ago' }
              ].map((activity, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">{activity.description}</p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Feature Limits Overview */}
        <Card>
          <CardHeader>
            <CardTitle>Account Features</CardTitle>
            <CardDescription>Your current plan capabilities</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {dashboardData?.features_available && Object.entries(dashboardData.features_available).map(([feature, limit]) => (
                <div key={feature} className="flex items-center justify-between">
                  <span className="text-sm font-medium capitalize">{feature.replace(/_/g, ' ')}</span>
                  <Badge variant={limit === 'unlimited' || limit === true ? 'default' : 'secondary'}>
                    {limit === true ? 'Available' : 
                     limit === false ? 'Not Available' : 
                     limit === 'unlimited' ? 'Unlimited' :
                     typeof limit === 'number' ? limit.toLocaleString() : limit}
                  </Badge>
                </div>
              )) || (
                <div className="text-center text-gray-500 py-4">
                  <p>Feature information loading...</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* AI Insights */}
      <Card>
        <CardHeader>
          <CardTitle>AI Insights</CardTitle>
          <CardDescription>Powered by Brainstorm AI</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <h4 className="font-semibold text-blue-900">Lead Quality Score</h4>
              <div className="mt-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-blue-700">Current Average</span>
                  <span className="font-bold text-blue-900">8.2/10</span>
                </div>
                <Progress value={82} className="mt-2" />
              </div>
              <p className="text-xs text-blue-600 mt-2">
                Your leads are 23% higher quality than industry average
              </p>
            </div>

            <div className="p-4 bg-green-50 rounded-lg">
              <h4 className="font-semibold text-green-900">Best Contact Time</h4>
              <div className="mt-2">
                <span className="text-2xl font-bold text-green-900">2-4 PM</span>
                <p className="text-sm text-green-700">Tuesday - Thursday</p>
              </div>
              <p className="text-xs text-green-600 mt-2">
                45% higher response rate during this window
              </p>
            </div>

            <div className="p-4 bg-purple-50 rounded-lg">
              <h4 className="font-semibold text-purple-900">Revenue Forecast</h4>
              <div className="mt-2">
                <span className="text-2xl font-bold text-purple-900">$35K</span>
                <p className="text-sm text-purple-700">Next 30 days</p>
              </div>
              <p className="text-xs text-purple-600 mt-2">
                Based on current pipeline and AI analysis
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

