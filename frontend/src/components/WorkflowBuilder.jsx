import { useState, useCallback, useRef } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import {
  Plus,
  Play,
  Pause,
  Save,
  Settings,
  Trash2,
  Mail,
  MessageSquare,
  Phone,
  Clock,
  Users,
  Tag,
  Zap,
  ArrowRight,
  Brain,
  Target,
  Filter,
  GitBranch
} from 'lucide-react'

export default function WorkflowBuilder() {
  const [workflow, setWorkflow] = useState({
    id: null,
    name: 'New Workflow',
    description: '',
    trigger: null,
    steps: [],
    status: 'draft'
  })
  
  const [selectedStep, setSelectedStep] = useState(null)
  const [showStepDialog, setShowStepDialog] = useState(false)
  const [draggedStep, setDraggedStep] = useState(null)
  const canvasRef = useRef(null)

  const triggerTypes = [
    { id: 'contact_created', name: 'Contact Created', icon: Users, description: 'When a new contact is added' },
    { id: 'form_submission', name: 'Form Submission', icon: Target, description: 'When a form is submitted' },
    { id: 'tag_added', name: 'Tag Added', icon: Tag, description: 'When a tag is added to contact' },
    { id: 'email_opened', name: 'Email Opened', icon: Mail, description: 'When contact opens an email' },
    { id: 'link_clicked', name: 'Link Clicked', icon: ArrowRight, description: 'When contact clicks a link' },
    { id: 'date_time', name: 'Date/Time', icon: Clock, description: 'At a specific date and time' },
    { id: 'inactivity', name: 'Inactivity', icon: Pause, description: 'After period of inactivity' }
  ]

  const stepTypes = [
    { id: 'send_email', name: 'Send Email', icon: Mail, category: 'Communication', description: 'Send an email to the contact' },
    { id: 'send_sms', name: 'Send SMS', icon: MessageSquare, category: 'Communication', description: 'Send SMS message' },
    { id: 'make_call', name: 'Make Call', icon: Phone, category: 'Communication', description: 'Schedule or make a call' },
    { id: 'wait', name: 'Wait', icon: Clock, category: 'Logic', description: 'Wait for specified time' },
    { id: 'add_tag', name: 'Add Tag', icon: Tag, category: 'Data', description: 'Add tag to contact' },
    { id: 'remove_tag', name: 'Remove Tag', icon: Tag, category: 'Data', description: 'Remove tag from contact' },
    { id: 'update_field', name: 'Update Field', icon: Settings, category: 'Data', description: 'Update contact field' },
    { id: 'condition', name: 'Condition', icon: GitBranch, category: 'Logic', description: 'Branch based on condition' },
    { id: 'ai_score', name: 'AI Score', icon: Brain, category: 'AI', description: 'Calculate AI lead score' },
    { id: 'ai_analyze', name: 'AI Analyze', icon: Zap, category: 'AI', description: 'AI analysis and insights' }
  ]

  const addStep = (stepType) => {
    const newStep = {
      id: Date.now(),
      type: stepType.id,
      name: stepType.name,
      icon: stepType.icon,
      config: {},
      position: { x: 100 + workflow.steps.length * 200, y: 200 },
      connections: []
    }
    
    setWorkflow(prev => ({
      ...prev,
      steps: [...prev.steps, newStep]
    }))
    setShowStepDialog(false)
  }

  const updateStep = (stepId, updates) => {
    setWorkflow(prev => ({
      ...prev,
      steps: prev.steps.map(step => 
        step.id === stepId ? { ...step, ...updates } : step
      )
    }))
  }

  const deleteStep = (stepId) => {
    setWorkflow(prev => ({
      ...prev,
      steps: prev.steps.filter(step => step.id !== stepId)
    }))
  }

  const connectSteps = (fromId, toId) => {
    setWorkflow(prev => ({
      ...prev,
      steps: prev.steps.map(step => 
        step.id === fromId 
          ? { ...step, connections: [...(step.connections || []), toId] }
          : step
      )
    }))
  }

  const saveWorkflow = async () => {
    try {
      const token = localStorage.getItem('auth_token')
      const response = await fetch('/api/ai/workflows', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          ...workflow,
          sub_account_id: 1
        })
      })
      
      if (response.ok) {
        const savedWorkflow = await response.json()
        setWorkflow(savedWorkflow)
        // Show success message
      }
    } catch (error) {
      console.error('Error saving workflow:', error)
    }
  }

  const activateWorkflow = async () => {
    try {
      const token = localStorage.getItem('auth_token')
      await fetch(`/api/ai/workflows/${workflow.id}/activate`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      })
      
      setWorkflow(prev => ({ ...prev, status: 'active' }))
    } catch (error) {
      console.error('Error activating workflow:', error)
    }
  }

  const StepCard = ({ step, onEdit, onDelete }) => {
    const IconComponent = step.icon
    
    return (
      <Card 
        className="w-48 cursor-move hover:shadow-lg transition-shadow border-2 border-dashed border-gray-300"
        style={{ 
          position: 'absolute', 
          left: step.position.x, 
          top: step.position.y 
        }}
        draggable
        onDragStart={() => setDraggedStep(step)}
      >
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="p-1 bg-blue-100 rounded">
                <IconComponent className="h-4 w-4 text-blue-600" />
              </div>
              <CardTitle className="text-sm">{step.name}</CardTitle>
            </div>
            <div className="flex space-x-1">
              <Button size="sm" variant="ghost" onClick={() => onEdit(step)}>
                <Settings className="h-3 w-3" />
              </Button>
              <Button size="sm" variant="ghost" onClick={() => onDelete(step.id)}>
                <Trash2 className="h-3 w-3" />
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="pt-0">
          <p className="text-xs text-gray-600">
            {step.config.description || 'Click to configure'}
          </p>
          {step.connections && step.connections.length > 0 && (
            <div className="mt-2 flex items-center">
              <ArrowRight className="h-3 w-3 text-gray-400" />
              <span className="text-xs text-gray-500 ml-1">
                {step.connections.length} connection(s)
              </span>
            </div>
          )}
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b">
        <div className="flex items-center space-x-4">
          <div>
            <h1 className="text-2xl font-bold">{workflow.name}</h1>
            <p className="text-gray-600">Visual workflow builder</p>
          </div>
          <Badge variant={workflow.status === 'active' ? 'default' : 'secondary'}>
            {workflow.status}
          </Badge>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button variant="outline" onClick={saveWorkflow}>
            <Save className="h-4 w-4 mr-2" />
            Save
          </Button>
          
          {workflow.status === 'draft' ? (
            <Button onClick={activateWorkflow}>
              <Play className="h-4 w-4 mr-2" />
              Activate
            </Button>
          ) : (
            <Button variant="outline">
              <Pause className="h-4 w-4 mr-2" />
              Pause
            </Button>
          )}
        </div>
      </div>

      <div className="flex flex-1">
        {/* Sidebar */}
        <div className="w-80 border-r bg-gray-50 p-4 overflow-y-auto">
          <div className="space-y-6">
            {/* Workflow Settings */}
            <div>
              <h3 className="font-medium mb-3">Workflow Settings</h3>
              <div className="space-y-3">
                <div>
                  <Label htmlFor="workflow-name">Name</Label>
                  <Input
                    id="workflow-name"
                    value={workflow.name}
                    onChange={(e) => setWorkflow(prev => ({ ...prev, name: e.target.value }))}
                  />
                </div>
                <div>
                  <Label htmlFor="workflow-description">Description</Label>
                  <Textarea
                    id="workflow-description"
                    value={workflow.description}
                    onChange={(e) => setWorkflow(prev => ({ ...prev, description: e.target.value }))}
                    rows={3}
                  />
                </div>
              </div>
            </div>

            {/* Trigger */}
            <div>
              <h3 className="font-medium mb-3">Trigger</h3>
              <Select 
                value={workflow.trigger?.id || ''} 
                onValueChange={(value) => {
                  const trigger = triggerTypes.find(t => t.id === value)
                  setWorkflow(prev => ({ ...prev, trigger }))
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select trigger" />
                </SelectTrigger>
                <SelectContent>
                  {triggerTypes.map((trigger) => {
                    const IconComponent = trigger.icon
                    return (
                      <SelectItem key={trigger.id} value={trigger.id}>
                        <div className="flex items-center space-x-2">
                          <IconComponent className="h-4 w-4" />
                          <div>
                            <div className="font-medium">{trigger.name}</div>
                            <div className="text-xs text-gray-500">{trigger.description}</div>
                          </div>
                        </div>
                      </SelectItem>
                    )
                  })}
                </SelectContent>
              </Select>
            </div>

            {/* Step Types */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-medium">Steps</h3>
                <Dialog open={showStepDialog} onOpenChange={setShowStepDialog}>
                  <DialogTrigger asChild>
                    <Button size="sm">
                      <Plus className="h-4 w-4 mr-1" />
                      Add Step
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-2xl">
                    <DialogHeader>
                      <DialogTitle>Add Workflow Step</DialogTitle>
                      <DialogDescription>
                        Choose a step type to add to your workflow
                      </DialogDescription>
                    </DialogHeader>
                    
                    <div className="grid grid-cols-2 gap-4 py-4">
                      {stepTypes.map((stepType) => {
                        const IconComponent = stepType.icon
                        return (
                          <Card 
                            key={stepType.id} 
                            className="cursor-pointer hover:shadow-md transition-shadow"
                            onClick={() => addStep(stepType)}
                          >
                            <CardHeader className="pb-2">
                              <div className="flex items-center space-x-2">
                                <div className="p-2 bg-blue-100 rounded">
                                  <IconComponent className="h-5 w-5 text-blue-600" />
                                </div>
                                <div>
                                  <CardTitle className="text-sm">{stepType.name}</CardTitle>
                                  <Badge variant="outline" className="text-xs">
                                    {stepType.category}
                                  </Badge>
                                </div>
                              </div>
                            </CardHeader>
                            <CardContent className="pt-0">
                              <p className="text-xs text-gray-600">{stepType.description}</p>
                            </CardContent>
                          </Card>
                        )
                      })}
                    </div>
                  </DialogContent>
                </Dialog>
              </div>
              
              <div className="text-sm text-gray-600">
                Drag and drop steps onto the canvas to build your workflow
              </div>
            </div>

            {/* AI Optimization */}
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center mb-2">
                <Brain className="h-5 w-5 text-blue-600 mr-2" />
                <h4 className="font-medium text-blue-800">AI Optimization</h4>
              </div>
              <p className="text-sm text-blue-700 mb-3">
                Let AI analyze and optimize your workflow for better performance
              </p>
              <Button size="sm" variant="outline" className="w-full">
                <Zap className="h-4 w-4 mr-2" />
                Optimize Workflow
              </Button>
            </div>
          </div>
        </div>

        {/* Canvas */}
        <div className="flex-1 relative overflow-hidden bg-gray-100">
          <div 
            ref={canvasRef}
            className="w-full h-full relative"
            onDrop={(e) => {
              e.preventDefault()
              if (draggedStep) {
                const rect = canvasRef.current.getBoundingClientRect()
                const x = e.clientX - rect.left
                const y = e.clientY - rect.top
                
                updateStep(draggedStep.id, {
                  position: { x: x - 96, y: y - 50 } // Center the card
                })
                setDraggedStep(null)
              }
            }}
            onDragOver={(e) => e.preventDefault()}
          >
            {/* Grid Background */}
            <div 
              className="absolute inset-0 opacity-20"
              style={{
                backgroundImage: `
                  linear-gradient(to right, #e5e7eb 1px, transparent 1px),
                  linear-gradient(to bottom, #e5e7eb 1px, transparent 1px)
                `,
                backgroundSize: '20px 20px'
              }}
            />

            {/* Trigger Card */}
            {workflow.trigger && (
              <Card className="absolute top-4 left-4 w-48 border-2 border-green-300 bg-green-50">
                <CardHeader className="pb-2">
                  <div className="flex items-center space-x-2">
                    <div className="p-1 bg-green-100 rounded">
                      <workflow.trigger.icon className="h-4 w-4 text-green-600" />
                    </div>
                    <CardTitle className="text-sm">Trigger</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="pt-0">
                  <p className="text-sm font-medium">{workflow.trigger.name}</p>
                  <p className="text-xs text-gray-600">{workflow.trigger.description}</p>
                </CardContent>
              </Card>
            )}

            {/* Workflow Steps */}
            {workflow.steps.map((step) => (
              <StepCard
                key={step.id}
                step={step}
                onEdit={setSelectedStep}
                onDelete={deleteStep}
              />
            ))}

            {/* Empty State */}
            {workflow.steps.length === 0 && !workflow.trigger && (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <Zap className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Build Your Workflow
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Start by selecting a trigger, then add steps to create your automation
                  </p>
                  <Button onClick={() => setShowStepDialog(true)}>
                    <Plus className="h-4 w-4 mr-2" />
                    Add First Step
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

