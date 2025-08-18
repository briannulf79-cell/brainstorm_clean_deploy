import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'
import {
  Brain,
  TrendingUp,
  TrendingDown,
  Target,
  Users,
  DollarSign,
  Zap,
  AlertTriangle,
  CheckCircle,
  Clock,
  Star,
  Lightbulb,
  BarChart3,
  PieChart,
  Activity,
  Sparkles,
  Bot,
  MessageSquare,
  Mail,
  Phone,
  Calendar,
  ArrowUp,
  ArrowDown,
  Minus
} from 'lucide-react'
import { LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart as RechartsPieChart, Cell, Pie, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function AIInsights() {
  const [insights, setInsights] = useState([])
  const [predictions, setPredictions] = useState([])
  const [leadScores, setLeadScores] = useState([])
  const [conversationAnalysis, setConversationAnalysis] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedTimeframe, setSelectedTimeframe] = useState('30d')

  useEffect(() => {
    fetchAIInsights()
  }, [selectedTimeframe])

  const fetchAIInsights = async () => {
    try {
      // Mock AI insights data
      setInsights([
        {
          id: 1,
          type: 'opportunity',
          title: 'High-Value Lead Identified',
          description: 'Sarah Johnson shows 94% likelihood of conversion based on engagement patterns',
          confidence: 94,
          impact: 'high',
          action: 'Schedule immediate follow-up call',
          created_at: '2024-01-15T14:30:00Z',
          status: 'new'
        },
        {
          id: 2,
          type: 'warning',
          title: 'Churn Risk Detected',
          description: 'Mike Chen has decreased engagement by 67% over the last 14 days',
          confidence: 78,
          impact: 'medium',
          action: 'Send re-engagement campaign',
          created_at: '2024-01-15T12:15:00Z',
          status: 'acknowledged'
        },
        {
          id: 3,
          type: 'optimization',
          title: 'Email Campaign Optimization',
          description: 'Subject lines with "Demo" have 34% higher open rates',
          confidence: 89,
          impact: 'medium',
          action: 'Update email templates',
          created_at: '2024-01-15T10:45:00Z',
          status: 'implemented'
        },
        {
          id: 4,
          type: 'trend',
          title: 'Seasonal Pattern Detected',
          description: 'Lead quality increases 23% during Tuesday-Thursday timeframe',
          confidence: 82,
          impact: 'low',
          action: 'Adjust ad spend schedule',
          created_at: '2024-01-15T09:20:00Z',
          status: 'new'
        }
      ])

      setPredictions([
        {
          metric: 'Revenue',
          current: 45000,
          predicted: 52000,
          change: 15.6,
          confidence: 87,
          timeframe: 'Next 30 days'
        },
        {
          metric: 'Conversions',
          current: 156,
          predicted: 189,
          change: 21.2,
          confidence: 91,
          timeframe: 'Next 30 days'
        },
        {
          metric: 'Lead Quality',
          current: 7.2,
          predicted: 8.1,
          change: 12.5,
          confidence: 79,
          timeframe: 'Next 30 days'
        },
        {
          metric: 'Churn Rate',
          current: 5.8,
          predicted: 4.2,
          change: -27.6,
          confidence: 84,
          timeframe: 'Next 30 days'
        }
      ])

      setLeadScores([
        {
          id: 1,
          name: 'Sarah Johnson',
          email: 'sarah@example.com',
          score: 94,
          factors: ['High engagement', 'Demo request', 'Enterprise company'],
          trend: 'up',
          last_activity: '2 hours ago'
        },
        {
          id: 2,
          name: 'David Wilson',
          email: 'david@techcorp.com',
          score: 87,
          factors: ['Multiple page views', 'Downloaded whitepaper', 'C-level title'],
          trend: 'up',
          last_activity: '4 hours ago'
        },
        {
          id: 3,
          name: 'Lisa Rodriguez',
          email: 'lisa@marketingagency.com',
          score: 76,
          factors: ['Pricing page visits', 'Email opens', 'Social media engagement'],
          trend: 'stable',
          last_activity: '1 day ago'
        },
        {
          id: 4,
          name: 'Mike Chen',
          email: 'mike@startup.com',
          score: 45,
          factors: ['Low engagement', 'No recent activity', 'Small company'],
          trend: 'down',
          last_activity: '5 days ago'
        }
      ])

      setConversationAnalysis([
        {
          channel: 'Email',
          total_conversations: 234,
          avg_sentiment: 0.72,
          response_time: '2h 15m',
          resolution_rate: 89,
          top_intents: ['Demo Request', 'Pricing', 'Support']
        },
        {
          channel: 'SMS',
          total_conversations: 156,
          avg_sentiment: 0.68,
          response_time: '45m',
          resolution_rate: 94,
          top_intents: ['Support', 'Scheduling', 'Follow-up']
        },
        {
          channel: 'Calls',
          total_conversations: 89,
          avg_sentiment: 0.81,
          response_time: '12m',
          resolution_rate: 96,
          top_intents: ['Demo', 'Consultation', 'Closing']
        }
      ])

    } catch (error) {
      console.error('Error fetching AI insights:', error)
    } finally {
      setLoading(false)
    }
  }

  const getInsightIcon = (type) => {
    switch (type) {
      case 'opportunity':
        return <Target className="h-5 w-5 text-green-600" />
      case 'warning':
        return <AlertTriangle className="h-5 w-5 text-yellow-600" />
      case 'optimization':
        return <Zap className="h-5 w-5 text-blue-600" />
      case 'trend':
        return <TrendingUp className="h-5 w-5 text-purple-600" />
      default:
        return <Brain className="h-5 w-5 text-gray-600" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'new':
        return 'bg-blue-100 text-blue-800'
      case 'acknowledged':
        return 'bg-yellow-100 text-yellow-800'
      case 'implemented':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'up':
        return <ArrowUp className="h-4 w-4 text-green-600" />
      case 'down':
        return <ArrowDown className="h-4 w-4 text-red-600" />
      default:
        return <Minus className="h-4 w-4 text-gray-600" />
    }
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(amount)
  }

  const getSentimentColor = (sentiment) => {
    if (sentiment >= 0.7) return 'text-green-600'
    if (sentiment >= 0.4) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getSentimentLabel = (sentiment) => {
    if (sentiment >= 0.7) return 'Positive'
    if (sentiment >= 0.4) return 'Neutral'
    return 'Negative'
  }

  // Sample data for charts
  const revenueData = [
    { month: 'Jan', actual: 42000, predicted: 45000 },
    { month: 'Feb', actual: 45000, predicted: 48000 },
    { month: 'Mar', actual: 48000, predicted: 52000 },
    { month: 'Apr', actual: null, predicted: 55000 },
    { month: 'May', actual: null, predicted: 58000 },
    { month: 'Jun', actual: null, predicted: 62000 }
  ]

  const leadScoreDistribution = [
    { range: '90-100', count: 12, color: '#10B981' },
    { range: '80-89', count: 28, color: '#3B82F6' },
    { range: '70-79', count: 45, color: '#F59E0B' },
    { range: '60-69', count: 34, color: '#EF4444' },
    { range: '0-59', count: 23, color: '#6B7280' }
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">AI Insights</h1>
          <p className="text-gray-600">Artificial intelligence-powered business insights and predictions</p>
        </div>
        
        <div className="flex items-center space-x-2">
          <Select value={selectedTimeframe} onValueChange={setSelectedTimeframe}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7d">Last 7 days</SelectItem>
              <SelectItem value="30d">Last 30 days</SelectItem>
              <SelectItem value="90d">Last 90 days</SelectItem>
            </SelectContent>
          </Select>
          
          <Button>
            <Sparkles className="h-4 w-4 mr-2" />
            Generate Report
          </Button>
        </div>
      </div>

      <Tabs defaultValue="insights" className="space-y-6">
        <TabsList>
          <TabsTrigger value="insights">Smart Insights</TabsTrigger>
          <TabsTrigger value="predictions">Predictions</TabsTrigger>
          <TabsTrigger value="lead-scoring">Lead Scoring</TabsTrigger>
          <TabsTrigger value="conversations">Conversation AI</TabsTrigger>
        </TabsList>

        <TabsContent value="insights" className="space-y-6">
          {/* AI Insights Cards */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {insights.map((insight) => (
              <Card key={insight.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      {getInsightIcon(insight.type)}
                      <div>
                        <CardTitle className="text-lg">{insight.title}</CardTitle>
                        <CardDescription>{insight.description}</CardDescription>
                      </div>
                    </div>
                    <Badge className={getStatusColor(insight.status)}>
                      {insight.status}
                    </Badge>
                  </div>
                </CardHeader>
                
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Brain className="h-4 w-4 text-gray-500" />
                      <span className="text-sm text-gray-600">Confidence</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Progress value={insight.confidence} className="w-20" />
                      <span className="text-sm font-medium">{insight.confidence}%</span>
                    </div>
                  </div>
                  
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <div className="flex items-center mb-1">
                      <Lightbulb className="h-4 w-4 text-blue-600 mr-2" />
                      <span className="text-sm font-medium text-blue-800">Recommended Action</span>
                    </div>
                    <p className="text-sm text-blue-700">{insight.action}</p>
                  </div>
                  
                  <div className="flex items-center justify-between pt-2 border-t">
                    <span className="text-xs text-gray-500">
                      {new Date(insight.created_at).toLocaleDateString()}
                    </span>
                    <div className="flex space-x-2">
                      <Button size="sm" variant="outline">
                        Dismiss
                      </Button>
                      <Button size="sm">
                        Take Action
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="predictions" className="space-y-6">
          {/* Predictions Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {predictions.map((prediction, index) => (
              <Card key={index}>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">{prediction.metric}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="flex items-baseline space-x-2">
                      <span className="text-2xl font-bold">
                        {prediction.metric === 'Revenue' ? formatCurrency(prediction.predicted) : prediction.predicted}
                      </span>
                      <div className={`flex items-center text-sm ${
                        prediction.change > 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {prediction.change > 0 ? <ArrowUp className="h-3 w-3" /> : <ArrowDown className="h-3 w-3" />}
                        {Math.abs(prediction.change)}%
                      </div>
                    </div>
                    
                    <div className="text-sm text-gray-600">
                      Current: {prediction.metric === 'Revenue' ? formatCurrency(prediction.current) : prediction.current}
                    </div>
                    
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-gray-500">{prediction.timeframe}</span>
                      <div className="flex items-center space-x-1">
                        <Brain className="h-3 w-3 text-gray-400" />
                        <span className="text-gray-500">{prediction.confidence}%</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Revenue Prediction Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Revenue Prediction</CardTitle>
              <CardDescription>Actual vs predicted revenue over time</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={revenueData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip formatter={(value) => formatCurrency(value)} />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="actual" 
                    stroke="#3B82F6" 
                    strokeWidth={2}
                    name="Actual Revenue"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="predicted" 
                    stroke="#10B981" 
                    strokeWidth={2}
                    strokeDasharray="5 5"
                    name="Predicted Revenue"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="lead-scoring" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Lead Score Distribution */}
            <Card>
              <CardHeader>
                <CardTitle>Lead Score Distribution</CardTitle>
                <CardDescription>Distribution of leads by AI score ranges</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <RechartsPieChart>
                    <Pie
                      data={leadScoreDistribution}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      dataKey="count"
                      label={({ range, count }) => `${range}: ${count}`}
                    >
                      {leadScoreDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </RechartsPieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Top Leads */}
            <Card>
              <CardHeader>
                <CardTitle>High-Value Leads</CardTitle>
                <CardDescription>Leads with highest AI scores</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {leadScores.map((lead) => (
                    <div key={lead.id} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <h4 className="font-medium">{lead.name}</h4>
                          {getTrendIcon(lead.trend)}
                        </div>
                        <p className="text-sm text-gray-600">{lead.email}</p>
                        <div className="flex flex-wrap gap-1 mt-2">
                          {lead.factors.slice(0, 2).map((factor, index) => (
                            <Badge key={index} variant="outline" className="text-xs">
                              {factor}
                            </Badge>
                          ))}
                        </div>
                      </div>
                      
                      <div className="text-right">
                        <div className="text-2xl font-bold text-blue-600">{lead.score}</div>
                        <div className="text-xs text-gray-500">{lead.last_activity}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="conversations" className="space-y-6">
          {/* Conversation Analysis */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {conversationAnalysis.map((analysis, index) => (
              <Card key={index}>
                <CardHeader>
                  <div className="flex items-center space-x-2">
                    {analysis.channel === 'Email' && <Mail className="h-5 w-5 text-blue-600" />}
                    {analysis.channel === 'SMS' && <MessageSquare className="h-5 w-5 text-green-600" />}
                    {analysis.channel === 'Calls' && <Phone className="h-5 w-5 text-purple-600" />}
                    <CardTitle>{analysis.channel}</CardTitle>
                  </div>
                </CardHeader>
                
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-gray-500">Conversations</div>
                      <div className="font-semibold">{analysis.total_conversations}</div>
                    </div>
                    <div>
                      <div className="text-gray-500">Resolution Rate</div>
                      <div className="font-semibold">{analysis.resolution_rate}%</div>
                    </div>
                    <div>
                      <div className="text-gray-500">Avg Response</div>
                      <div className="font-semibold">{analysis.response_time}</div>
                    </div>
                    <div>
                      <div className="text-gray-500">Sentiment</div>
                      <div className={`font-semibold ${getSentimentColor(analysis.avg_sentiment)}`}>
                        {getSentimentLabel(analysis.avg_sentiment)}
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <div className="text-sm text-gray-500 mb-2">Top Intents</div>
                    <div className="flex flex-wrap gap-1">
                      {analysis.top_intents.map((intent, idx) => (
                        <Badge key={idx} variant="secondary" className="text-xs">
                          {intent}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* AI Conversation Insights */}
          <Card>
            <CardHeader>
              <CardTitle>AI Conversation Insights</CardTitle>
              <CardDescription>Advanced analysis of customer conversations</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-600">87%</div>
                  <div className="text-sm text-gray-600">Positive Sentiment</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">2.3x</div>
                  <div className="text-sm text-gray-600">Faster Resolution</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-purple-600">94%</div>
                  <div className="text-sm text-gray-600">Intent Accuracy</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-600">156</div>
                  <div className="text-sm text-gray-600">Auto-Responses</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

