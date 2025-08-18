import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import {
  Zap,
  Plus,
  Play,
  Pause,
  Settings,
  Brain,
  Users,
  Mail,
  MessageSquare,
  Clock,
  TrendingUp,
  CheckCircle,
  AlertCircle,
  Workflow
} from 'lucide-react'

export default function Automation() {
  const [workflows, setWorkflows] = useState([])
  const [insights, setInsights] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAutomationData()
  }, [])

  const fetchAutomationData = async () => {
    try {
      const token = localStorage.getItem('auth_token')
      
      // Fetch workflows
      const workflowsResponse = await fetch('/api/ai/workflows?sub_account_id=1', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      const workflowsData = await workflowsResponse.json()
      
      // Mock data for demo
      setWorkflows([
        {
          id: 1,
          name: 'Welcome Email Series',
          description: 'Automated welcome sequence for new leads',
          trigger_type: 'contact_created',
          status: 'active',
          is_ai_optimized: true,
          executions_count: 247,
          success_rate: 94.3,
          created_at: '2024-01-15T10:00:00Z',
          steps_count: 5
        },
        {
          id: 2,
          name: 'Lead Scoring & Nurture',
          description: 'AI-powered lead scoring with personalized follow-up',
          trigger_type: 'form_submission',
          status: 'active',
          is_ai_optimized: true,
          executions_count: 156,
          success_rate: 87.2,
          created_at: '2024-01-14T14:30:00Z',
          steps_count: 8
        },
        {
          id: 3,
          name: 'Demo Request Follow-up',
          description: 'Immediate response and scheduling for demo requests',
          trigger_type: 'tag_added',
          status: 'active',
          is_ai_optimized: false,
          executions_count: 89,
          success_rate: 91.0,
          created_at: '2024-01-13T09:15:00Z',
          steps_count: 3
        },
        {
          id: 4,
          name: 'Customer Onboarding',
          description: 'Complete onboarding sequence for new customers',
          trigger_type: 'opportunity_won',
          status: 'draft',
          is_ai_optimized: false,
          executions_count: 0,
          success_rate: 0,
          created_at: '2024-01-12T16:45:00Z',
          steps_count: 12
        },
        {
          id: 5,
          name: 'Re-engagement Campaign',
          description: 'Win back inactive leads with personalized content',
          trigger_type: 'inactivity_detected',
          status: 'paused',
          is_ai_optimized: true,
          executions_count: 78,
          success_rate: 76.9,
          created_at: '2024-01-11T11:20:00Z',
          steps_count: 6
        }
      ])

      // Fetch AI insights
      const insightsResponse = await fetch('/api/ai/insights?sub_account_id=1&category=automation', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      const insightsData = await insightsResponse.json()
      setInsights(insightsData.insights || [])

    } catch (error) {
      console.error('Error fetching automation data:', error)
    } finally {
      setLoading(false)
    }
  }

  const getTriggerIcon = (triggerType) => {
    switch (triggerType) {
      case 'contact_created':
        return <Users className="h-4 w-4" />
      case 'form_submission':
        return <CheckCircle className="h-4 w-4" />
      case 'tag_added':
        return <AlertCircle className="h-4 w-4" />
      case 'opportunity_won':
        return <TrendingUp className="h-4 w-4" />
      case 'inactivity_detected':
        return <Clock className="h-4 w-4" />
      default:
        return <Workflow className="h-4 w-4" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'paused':
        return 'bg-yellow-100 text-yellow-800'
      case 'draft':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const formatTriggerType = (triggerType) => {
    return triggerType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  const activeWorkflows = workflows.filter(w => w.status === 'active').length
  const totalExecutions = workflows.reduce((sum, workflow) => sum + workflow.executions_count, 0)
  const avgSuccessRate = workflows.length > 0 
    ? workflows.reduce((sum, workflow) => sum + workflow.success_rate, 0) / workflows.length 
    : 0

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Automation</h1>
          <p className="text-gray-600">Build intelligent workflows with AI-powered optimization</p>
        </div>
        
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Create Workflow
        </Button>
      </div>

      {/* Automation Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Workflows</CardTitle>
            <Zap className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{activeWorkflows}</div>
            <p className="text-xs text-muted-foreground">
              {workflows.length} total workflows
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Executions</CardTitle>
            <Play className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalExecutions.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              This month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{avgSuccessRate.toFixed(1)}%</div>
            <p className="text-xs text-muted-foreground">
              Average across all workflows
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">AI Optimized</CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {workflows.filter(w => w.is_ai_optimized).length}
            </div>
            <p className="text-xs text-muted-foreground">
              Workflows enhanced by AI
            </p>
          </CardContent>
        </Card>
      </div>

      {/* AI Optimization Insights */}
      {insights.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Brain className="h-5 w-5 mr-2 text-blue-600" />
              AI Optimization Suggestions
            </CardTitle>
            <CardDescription>
              Intelligent recommendations to improve your automation performance
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {insights.slice(0, 2).map((insight, index) => (
                <div key={index} className="flex items-start space-x-4 p-4 bg-blue-50 rounded-lg">
                  <div className="p-2 bg-blue-100 rounded-full">
                    <Zap className="h-4 w-4 text-blue-600" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-medium">{insight.title}</h4>
                    <p className="text-sm text-gray-600 mt-1">{insight.description}</p>
                    <div className="flex items-center mt-2 space-x-4">
                      <Badge variant="secondary">
                        {insight.priority} priority
                      </Badge>
                      <span className="text-sm text-green-600 font-medium">
                        +{insight.estimated_value?.toLocaleString()} potential value
                      </span>
                    </div>
                  </div>
                  <Button size="sm" variant="outline">
                    Apply
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Workflows List */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {workflows.map((workflow) => (
          <Card key={workflow.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    {getTriggerIcon(workflow.trigger_type)}
                  </div>
                  <div>
                    <CardTitle className="text-lg flex items-center">
                      {workflow.name}
                      {workflow.is_ai_optimized && (
                        <Brain className="h-4 w-4 ml-2 text-blue-600" />
                      )}
                    </CardTitle>
                    <CardDescription className="mt-1">
                      {workflow.description}
                    </CardDescription>
                  </div>
                </div>
                
                <Badge className={getStatusColor(workflow.status)}>
                  {workflow.status}
                </Badge>
              </div>
            </CardHeader>
            
            <CardContent className="space-y-4">
              {/* Workflow Details */}
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <Badge variant="outline">
                    {formatTriggerType(workflow.trigger_type)}
                  </Badge>
                  <span className="text-gray-500">
                    {workflow.steps_count} steps
                  </span>
                </div>
                
                <div className="text-gray-500">
                  {workflow.executions_count} executions
                </div>
              </div>

              {/* Performance Metrics */}
              {workflow.executions_count > 0 && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Success Rate</span>
                    <span className="text-sm font-semibold text-green-600">
                      {workflow.success_rate}%
                    </span>
                  </div>
                  <Progress value={workflow.success_rate} className="h-2" />
                </div>
              )}

              {/* AI Optimization Status */}
              {workflow.is_ai_optimized && (
                <div className="flex items-center space-x-2 p-2 bg-blue-50 rounded-lg">
                  <Brain className="h-4 w-4 text-blue-600" />
                  <span className="text-sm text-blue-800 font-medium">
                    AI Optimized for better performance
                  </span>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-2 border-t">
                <div className="flex space-x-2">
                  {workflow.status === 'active' ? (
                    <Button size="sm" variant="outline">
                      <Pause className="h-3 w-3 mr-1" />
                      Pause
                    </Button>
                  ) : workflow.status === 'paused' ? (
                    <Button size="sm" variant="outline">
                      <Play className="h-3 w-3 mr-1" />
                      Resume
                    </Button>
                  ) : workflow.status === 'draft' ? (
                    <Button size="sm">
                      <Play className="h-3 w-3 mr-1" />
                      Activate
                    </Button>
                  ) : null}
                  
                  {!workflow.is_ai_optimized && workflow.executions_count > 10 && (
                    <Button size="sm" variant="outline" className="text-blue-600">
                      <Brain className="h-3 w-3 mr-1" />
                      AI Optimize
                    </Button>
                  )}
                </div>
                
                <Button size="sm" variant="ghost">
                  <Settings className="h-3 w-3 mr-1" />
                  Edit
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {workflows.length === 0 && (
        <Card>
          <CardContent className="text-center py-12">
            <Zap className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No workflows yet</h3>
            <p className="text-gray-600 mb-4">
              Create your first automation workflow to streamline your business processes
            </p>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Create Workflow
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

