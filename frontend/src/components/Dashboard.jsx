import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts'
import {
  Users,
  DollarSign,
  TrendingUp,
  Mail,
  Phone,
  Calendar,
  Brain,
  Zap,
  Target,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react'

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null)
  const [insights, setInsights] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('auth_token')
      
      // Fetch metrics
      const metricsResponse = await fetch('/api/dashboard/metrics?sub_account_id=1', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      const metricsData = await metricsResponse.json()
      setMetrics(metricsData.metrics)

      // Fetch AI insights
      const insightsResponse = await fetch('/api/ai/insights?sub_account_id=1', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      const insightsData = await insightsResponse.json()
      setInsights(insightsData.insights || [])

    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  // Mock data for charts
  const leadsOverTime = [
    { date: '2024-01-01', leads: 45 },
    { date: '2024-01-02', leads: 52 },
    { date: '2024-01-03', leads: 48 },
    { date: '2024-01-04', leads: 61 },
    { date: '2024-01-05', leads: 55 },
    { date: '2024-01-06', leads: 67 },
    { date: '2024-01-07', leads: 73 }
  ]

  const pipelineData = [
    { stage: 'Lead', count: 45, value: 125000 },
    { stage: 'Qualified', count: 32, value: 89000 },
    { stage: 'Proposal', count: 18, value: 67000 },
    { stage: 'Negotiation', count: 12, value: 45000 },
    { stage: 'Closed Won', count: 8, value: 32000 }
  ]

  const campaignPerformance = [
    { name: 'Email Campaign A', impressions: 25000, clicks: 2500, conversions: 125 },
    { name: 'Social Media B', impressions: 18000, clicks: 1800, conversions: 90 },
    { name: 'Google Ads C', impressions: 32000, clicks: 3200, conversions: 160 },
    { name: 'LinkedIn D', impressions: 12000, clicks: 1200, conversions: 60 }
  ]

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 rounded-lg p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">Welcome to Brainstorm AI Kit</h1>
            <p className="text-blue-100">
              Your AI-powered business growth platform is ready to accelerate your success.
            </p>
          </div>
          <Brain className="h-16 w-16 text-blue-200" />
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Contacts</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics?.total_contacts || 0}</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-600 flex items-center">
                <ArrowUpRight className="h-3 w-3 mr-1" />
                +{metrics?.new_contacts || 0} this month
              </span>
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Revenue</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${metrics?.total_revenue?.toLocaleString() || '0'}
            </div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-600 flex items-center">
                <ArrowUpRight className="h-3 w-3 mr-1" />
                +12% from last month
              </span>
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics?.conversion_rate || 0}%</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-green-600 flex items-center">
                <ArrowUpRight className="h-3 w-3 mr-1" />
                +2.1% from last month
              </span>
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Campaigns</CardTitle>
            <Mail className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics?.active_campaigns || 0}</div>
            <p className="text-xs text-muted-foreground">
              <span className="text-blue-600">
                Running across all channels
              </span>
            </p>
          </CardContent>
        </Card>
      </div>

      {/* AI Insights */}
      {insights.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Brain className="h-5 w-5 mr-2 text-blue-600" />
              AI-Powered Insights
            </CardTitle>
            <CardDescription>
              Intelligent recommendations to optimize your business performance
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {insights.slice(0, 3).map((insight, index) => (
                <div key={index} className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg">
                  <div className={`
                    p-2 rounded-full
                    ${insight.priority === 'high' ? 'bg-red-100 text-red-600' : 
                      insight.priority === 'medium' ? 'bg-yellow-100 text-yellow-600' : 
                      'bg-blue-100 text-blue-600'}
                  `}>
                    <Zap className="h-4 w-4" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-medium">{insight.title}</h4>
                    <p className="text-sm text-gray-600 mt-1">{insight.description}</p>
                    <div className="flex items-center mt-2 space-x-4">
                      <Badge variant={insight.priority === 'high' ? 'destructive' : 'secondary'}>
                        {insight.priority} priority
                      </Badge>
                      {insight.estimated_value > 0 && (
                        <span className="text-sm text-green-600 font-medium">
                          +${insight.estimated_value.toLocaleString()} potential
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Leads Over Time */}
        <Card>
          <CardHeader>
            <CardTitle>Lead Generation Trend</CardTitle>
            <CardDescription>Daily lead acquisition over the past week</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={leadsOverTime}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="leads" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Pipeline Overview */}
        <Card>
          <CardHeader>
            <CardTitle>Sales Pipeline</CardTitle>
            <CardDescription>Opportunities by stage</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={pipelineData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="stage" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Campaign Performance */}
      <Card>
        <CardHeader>
          <CardTitle>Campaign Performance</CardTitle>
          <CardDescription>Recent marketing campaign results</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={campaignPerformance}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="impressions" fill="#3b82f6" name="Impressions" />
              <Bar dataKey="clicks" fill="#10b981" name="Clicks" />
              <Bar dataKey="conversions" fill="#f59e0b" name="Conversions" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>Common tasks to boost your productivity</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button className="h-20 flex flex-col items-center justify-center space-y-2">
              <Users className="h-6 w-6" />
              <span>Add Contact</span>
            </Button>
            <Button variant="outline" className="h-20 flex flex-col items-center justify-center space-y-2">
              <Mail className="h-6 w-6" />
              <span>Create Campaign</span>
            </Button>
            <Button variant="outline" className="h-20 flex flex-col items-center justify-center space-y-2">
              <Zap className="h-6 w-6" />
              <span>Build Automation</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

