import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Progress } from '@/components/ui/progress'
import {
  DragDropContext,
  Droppable,
  Draggable
} from 'react-beautiful-dnd'
import {
  GitBranch,
  Plus,
  DollarSign,
  Calendar,
  User,
  Building,
  TrendingUp,
  Clock,
  Target
} from 'lucide-react'

export default function Pipelines() {
  const [pipelineData, setPipelineData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPipelineData()
  }, [])

  const fetchPipelineData = async () => {
    try {
      const token = localStorage.getItem('auth_token')
      const response = await fetch('/api/pipelines/1/opportunities', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      const data = await response.json()
      setPipelineData(data)
    } catch (error) {
      console.error('Error fetching pipeline data:', error)
      // Mock data for demo
      setPipelineData({
        pipeline: {
          name: 'Sales Pipeline',
          stages: [
            { name: 'Lead', order: 0, color: '#3b82f6', probability: 10 },
            { name: 'Qualified', order: 1, color: '#10b981', probability: 25 },
            { name: 'Proposal', order: 2, color: '#f59e0b', probability: 50 },
            { name: 'Negotiation', order: 3, color: '#ef4444', probability: 75 },
            { name: 'Closed Won', order: 4, color: '#22c55e', probability: 100 }
          ]
        },
        stages: {
          'Lead': {
            stage_info: { name: 'Lead', color: '#3b82f6' },
            opportunities: [
              { id: 1, title: 'Acme Corp Deal', value: 25000, contact_id: 1, probability: 10, created_at: '2024-01-15T10:00:00Z' },
              { id: 2, title: 'Tech Solutions Inc', value: 45000, contact_id: 2, probability: 15, created_at: '2024-01-14T14:30:00Z' },
              { id: 3, title: 'Digital Marketing Pro', value: 15000, contact_id: 3, probability: 20, created_at: '2024-01-13T09:15:00Z' }
            ],
            count: 3,
            total_value: 85000
          },
          'Qualified': {
            stage_info: { name: 'Qualified', color: '#10b981' },
            opportunities: [
              { id: 4, title: 'Enterprise Solutions', value: 75000, contact_id: 4, probability: 30, created_at: '2024-01-12T11:20:00Z' },
              { id: 5, title: 'Startup Accelerator', value: 35000, contact_id: 5, probability: 25, created_at: '2024-01-11T16:45:00Z' }
            ],
            count: 2,
            total_value: 110000
          },
          'Proposal': {
            stage_info: { name: 'Proposal', color: '#f59e0b' },
            opportunities: [
              { id: 6, title: 'Growth Solutions LLC', value: 55000, contact_id: 6, probability: 60, created_at: '2024-01-10T13:10:00Z' }
            ],
            count: 1,
            total_value: 55000
          },
          'Negotiation': {
            stage_info: { name: 'Negotiation', color: '#ef4444' },
            opportunities: [
              { id: 7, title: 'Innovation Hub', value: 95000, contact_id: 7, probability: 80, created_at: '2024-01-09T08:30:00Z' }
            ],
            count: 1,
            total_value: 95000
          },
          'Closed Won': {
            stage_info: { name: 'Closed Won', color: '#22c55e' },
            opportunities: [
              { id: 8, title: 'Success Stories Inc', value: 65000, contact_id: 8, probability: 100, created_at: '2024-01-08T15:20:00Z' }
            ],
            count: 1,
            total_value: 65000
          }
        }
      })
    } finally {
      setLoading(false)
    }
  }

  const handleDragEnd = async (result) => {
    if (!result.destination) return

    const { source, destination, draggableId } = result
    
    if (source.droppableId === destination.droppableId) return

    // Update opportunity stage
    try {
      const token = localStorage.getItem('auth_token')
      await fetch(`/api/pipelines/opportunities/${draggableId}/stage`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          stage: destination.droppableId,
          probability: pipelineData.pipeline.stages.find(s => s.name === destination.droppableId)?.probability || 50
        })
      })
      
      // Refresh data
      fetchPipelineData()
    } catch (error) {
      console.error('Error updating opportunity stage:', error)
    }
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(amount)
  }

  const getDaysInStage = (createdAt) => {
    const created = new Date(createdAt)
    const now = new Date()
    const diffTime = Math.abs(now - created)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    return diffDays
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  const totalValue = Object.values(pipelineData.stages).reduce((sum, stage) => sum + stage.total_value, 0)
  const totalOpportunities = Object.values(pipelineData.stages).reduce((sum, stage) => sum + stage.count, 0)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Sales Pipeline</h1>
          <p className="text-gray-600">Track and manage your sales opportunities</p>
        </div>
        
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Add Opportunity
        </Button>
      </div>

      {/* Pipeline Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Pipeline Value</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(totalValue)}</div>
            <p className="text-xs text-muted-foreground">
              Across all stages
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Opportunities</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalOpportunities}</div>
            <p className="text-xs text-muted-foreground">
              Active deals
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Deal Size</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCurrency(totalOpportunities > 0 ? totalValue / totalOpportunities : 0)}
            </div>
            <p className="text-xs text-muted-foreground">
              Per opportunity
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Win Rate</CardTitle>
            <GitBranch className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">23.5%</div>
            <p className="text-xs text-muted-foreground">
              Last 30 days
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Pipeline Board */}
      <DragDropContext onDragEnd={handleDragEnd}>
        <div className="flex space-x-6 overflow-x-auto pb-4">
          {pipelineData.pipeline.stages.map((stage) => {
            const stageData = pipelineData.stages[stage.name] || { opportunities: [], count: 0, total_value: 0 }
            
            return (
              <div key={stage.name} className="flex-shrink-0 w-80">
                <Card>
                  <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg flex items-center">
                        <div 
                          className="w-3 h-3 rounded-full mr-2"
                          style={{ backgroundColor: stage.color }}
                        />
                        {stage.name}
                      </CardTitle>
                      <Badge variant="secondary">
                        {stageData.count}
                      </Badge>
                    </div>
                    <CardDescription>
                      {formatCurrency(stageData.total_value)} total value
                    </CardDescription>
                  </CardHeader>
                  
                  <CardContent>
                    <Droppable droppableId={stage.name}>
                      {(provided, snapshot) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.droppableProps}
                          className={`space-y-3 min-h-[200px] p-2 rounded-lg transition-colors ${
                            snapshot.isDraggingOver ? 'bg-blue-50' : ''
                          }`}
                        >
                          {stageData.opportunities.map((opportunity, index) => (
                            <Draggable
                              key={opportunity.id}
                              draggableId={opportunity.id.toString()}
                              index={index}
                            >
                              {(provided, snapshot) => (
                                <div
                                  ref={provided.innerRef}
                                  {...provided.draggableProps}
                                  {...provided.dragHandleProps}
                                  className={`bg-white border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow cursor-move ${
                                    snapshot.isDragging ? 'shadow-lg' : ''
                                  }`}
                                >
                                  <div className="space-y-3">
                                    <div>
                                      <h4 className="font-medium text-gray-900">
                                        {opportunity.title}
                                      </h4>
                                      <p className="text-sm text-gray-600 flex items-center mt-1">
                                        <Building className="h-3 w-3 mr-1" />
                                        Contact #{opportunity.contact_id}
                                      </p>
                                    </div>
                                    
                                    <div className="flex items-center justify-between">
                                      <span className="text-lg font-semibold text-green-600">
                                        {formatCurrency(opportunity.value)}
                                      </span>
                                      <Badge variant="outline" className="text-xs">
                                        {opportunity.probability}%
                                      </Badge>
                                    </div>
                                    
                                    <div className="flex items-center justify-between text-xs text-gray-500">
                                      <div className="flex items-center">
                                        <Clock className="h-3 w-3 mr-1" />
                                        {getDaysInStage(opportunity.created_at)} days
                                      </div>
                                      <div className="flex items-center">
                                        <User className="h-3 w-3 mr-1" />
                                        Unassigned
                                      </div>
                                    </div>
                                    
                                    <Progress 
                                      value={opportunity.probability} 
                                      className="h-1"
                                    />
                                  </div>
                                </div>
                              )}
                            </Draggable>
                          ))}
                          {provided.placeholder}
                          
                          {stageData.opportunities.length === 0 && (
                            <div className="text-center py-8 text-gray-400">
                              <Target className="h-8 w-8 mx-auto mb-2" />
                              <p className="text-sm">No opportunities</p>
                            </div>
                          )}
                        </div>
                      )}
                    </Droppable>
                  </CardContent>
                </Card>
              </div>
            )
          })}
        </div>
      </DragDropContext>
    </div>
  )
}

