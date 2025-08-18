import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import {
  Mail,
  MessageSquare,
  Phone,
  Plus,
  Play,
  Pause,
  BarChart3,
  Users,
  Eye,
  MousePointer,
  TrendingUp,
  Calendar
} from 'lucide-react'

export default function Campaigns() {
  const [campaigns, setCampaigns] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCampaigns()
  }, [])

  const fetchCampaigns = async () => {
    try {
      // Mock data for demo - in real app, this would fetch from API
      setCampaigns([
        {
          id: 1,
          name: 'AI Solutions Newsletter',
          type: 'email',
          status: 'active',
          subject: 'Transform Your Business with AI Automation',
          sent_count: 2847,
          open_rate: 24.5,
          click_rate: 3.2,
          conversion_rate: 1.8,
          created_at: '2024-01-15T10:00:00Z',
          scheduled_at: '2024-01-16T09:00:00Z'
        },
        {
          id: 2,
          name: 'Lead Nurture Sequence',
          type: 'mixed',
          status: 'active',
          subject: 'Your AI Journey Starts Here',
          sent_count: 1523,
          open_rate: 31.2,
          click_rate: 4.7,
          conversion_rate: 2.3,
          created_at: '2024-01-14T14:30:00Z',
          scheduled_at: null
        },
        {
          id: 3,
          name: 'Product Demo Follow-up',
          type: 'sms',
          status: 'completed',
          subject: 'Thanks for your interest in Brainstorm AI Kit',
          sent_count: 456,
          open_rate: 98.2,
          click_rate: 12.4,
          conversion_rate: 5.1,
          created_at: '2024-01-13T09:15:00Z',
          scheduled_at: null
        },
        {
          id: 4,
          name: 'Webinar Invitation',
          type: 'email',
          status: 'draft',
          subject: 'Join Our Exclusive AI Masterclass',
          sent_count: 0,
          open_rate: 0,
          click_rate: 0,
          conversion_rate: 0,
          created_at: '2024-01-12T16:45:00Z',
          scheduled_at: '2024-01-18T10:00:00Z'
        },
        {
          id: 5,
          name: 'Customer Success Stories',
          type: 'email',
          status: 'paused',
          subject: 'See How Our Clients Achieved 300% Growth',
          sent_count: 1876,
          open_rate: 28.9,
          click_rate: 5.3,
          conversion_rate: 2.7,
          created_at: '2024-01-11T11:20:00Z',
          scheduled_at: null
        }
      ])
    } catch (error) {
      console.error('Error fetching campaigns:', error)
    } finally {
      setLoading(false)
    }
  }

  const getCampaignIcon = (type) => {
    switch (type) {
      case 'email':
        return <Mail className="h-4 w-4" />
      case 'sms':
        return <MessageSquare className="h-4 w-4" />
      case 'mixed':
        return <Phone className="h-4 w-4" />
      default:
        return <Mail className="h-4 w-4" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'paused':
        return 'bg-yellow-100 text-yellow-800'
      case 'completed':
        return 'bg-blue-100 text-blue-800'
      case 'draft':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'Not scheduled'
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  const totalSent = campaigns.reduce((sum, campaign) => sum + campaign.sent_count, 0)
  const avgOpenRate = campaigns.length > 0 
    ? campaigns.reduce((sum, campaign) => sum + campaign.open_rate, 0) / campaigns.length 
    : 0
  const avgClickRate = campaigns.length > 0 
    ? campaigns.reduce((sum, campaign) => sum + campaign.click_rate, 0) / campaigns.length 
    : 0

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Campaigns</h1>
          <p className="text-gray-600">Create and manage your marketing campaigns</p>
        </div>
        
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Create Campaign
        </Button>
      </div>

      {/* Campaign Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Campaigns</CardTitle>
            <Mail className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{campaigns.length}</div>
            <p className="text-xs text-muted-foreground">
              {campaigns.filter(c => c.status === 'active').length} active
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Messages Sent</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalSent.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              Across all campaigns
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg. Open Rate</CardTitle>
            <Eye className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{avgOpenRate.toFixed(1)}%</div>
            <p className="text-xs text-muted-foreground">
              Industry avg: 21.3%
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Avg. Click Rate</CardTitle>
            <MousePointer className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{avgClickRate.toFixed(1)}%</div>
            <p className="text-xs text-muted-foreground">
              Industry avg: 2.6%
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Campaigns List */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {campaigns.map((campaign) => (
          <Card key={campaign.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    {getCampaignIcon(campaign.type)}
                  </div>
                  <div>
                    <CardTitle className="text-lg">{campaign.name}</CardTitle>
                    <CardDescription className="mt-1">
                      {campaign.subject}
                    </CardDescription>
                  </div>
                </div>
                
                <Badge className={getStatusColor(campaign.status)}>
                  {campaign.status}
                </Badge>
              </div>
            </CardHeader>
            
            <CardContent className="space-y-4">
              {/* Campaign Type and Schedule */}
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <Badge variant="outline" className="capitalize">
                    {campaign.type}
                  </Badge>
                  <span className="text-gray-500">
                    {campaign.sent_count.toLocaleString()} sent
                  </span>
                </div>
                
                <div className="flex items-center text-gray-500">
                  <Calendar className="h-3 w-3 mr-1" />
                  {formatDate(campaign.scheduled_at)}
                </div>
              </div>

              {/* Performance Metrics */}
              {campaign.sent_count > 0 && (
                <div className="space-y-3">
                  <div className="grid grid-cols-3 gap-4 text-center">
                    <div>
                      <div className="text-lg font-semibold text-blue-600">
                        {campaign.open_rate}%
                      </div>
                      <div className="text-xs text-gray-500">Open Rate</div>
                    </div>
                    <div>
                      <div className="text-lg font-semibold text-green-600">
                        {campaign.click_rate}%
                      </div>
                      <div className="text-xs text-gray-500">Click Rate</div>
                    </div>
                    <div>
                      <div className="text-lg font-semibold text-purple-600">
                        {campaign.conversion_rate}%
                      </div>
                      <div className="text-xs text-gray-500">Conversion</div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span>Open Rate</span>
                      <span>{campaign.open_rate}%</span>
                    </div>
                    <Progress value={campaign.open_rate} className="h-1" />
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-2 border-t">
                <div className="flex space-x-2">
                  {campaign.status === 'active' ? (
                    <Button size="sm" variant="outline">
                      <Pause className="h-3 w-3 mr-1" />
                      Pause
                    </Button>
                  ) : campaign.status === 'paused' ? (
                    <Button size="sm" variant="outline">
                      <Play className="h-3 w-3 mr-1" />
                      Resume
                    </Button>
                  ) : campaign.status === 'draft' ? (
                    <Button size="sm">
                      <Play className="h-3 w-3 mr-1" />
                      Launch
                    </Button>
                  ) : null}
                  
                  <Button size="sm" variant="outline">
                    <BarChart3 className="h-3 w-3 mr-1" />
                    Analytics
                  </Button>
                </div>
                
                <Button size="sm" variant="ghost">
                  Edit
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {campaigns.length === 0 && (
        <Card>
          <CardContent className="text-center py-12">
            <Mail className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No campaigns yet</h3>
            <p className="text-gray-600 mb-4">
              Create your first marketing campaign to start engaging with your audience
            </p>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Create Campaign
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

