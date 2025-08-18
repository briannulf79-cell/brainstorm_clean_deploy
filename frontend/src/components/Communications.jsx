import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
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
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'
import {
  Mail,
  MessageSquare,
  Phone,
  Send,
  Search,
  Filter,
  Archive,
  Star,
  Reply,
  Forward,
  MoreHorizontal,
  Paperclip,
  Smile,
  Clock,
  CheckCircle,
  AlertCircle,
  User,
  Calendar,
  PhoneCall,
  Video,
  Mic,
  MicOff,
  PhoneOff,
  Brain,
  Zap,
  TrendingUp
} from 'lucide-react'

export default function Communications() {
  const [conversations, setConversations] = useState([])
  const [selectedConversation, setSelectedConversation] = useState(null)
  const [activeTab, setActiveTab] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [newMessage, setNewMessage] = useState('')
  const [loading, setLoading] = useState(true)
  const [showNewConversation, setShowNewConversation] = useState(false)

  useEffect(() => {
    fetchConversations()
  }, [])

  const fetchConversations = async () => {
    try {
      // Mock data for demo
      setConversations([
        {
          id: 1,
          contact: {
            id: 1,
            name: 'Sarah Johnson',
            email: 'sarah@example.com',
            phone: '+1 (555) 123-4567',
            avatar: null
          },
          type: 'email',
          subject: 'Product Demo Request',
          last_message: 'Hi, I\'d like to schedule a demo of your platform. When would be a good time?',
          last_message_at: '2024-01-15T14:30:00Z',
          unread_count: 2,
          status: 'open',
          assigned_to: 'Demo User',
          tags: ['hot-lead', 'demo-request'],
          ai_sentiment: 'positive',
          ai_priority: 'high',
          messages: [
            {
              id: 1,
              from: 'sarah@example.com',
              to: 'demo@brainstormaikit.com',
              content: 'Hi, I saw your website and I\'m interested in learning more about your AI-powered CRM platform.',
              timestamp: '2024-01-15T13:00:00Z',
              type: 'email',
              direction: 'inbound'
            },
            {
              id: 2,
              from: 'demo@brainstormaikit.com',
              to: 'sarah@example.com',
              content: 'Thank you for your interest! I\'d be happy to show you how our platform can help grow your business. Are you available for a 30-minute demo this week?',
              timestamp: '2024-01-15T13:15:00Z',
              type: 'email',
              direction: 'outbound'
            },
            {
              id: 3,
              from: 'sarah@example.com',
              to: 'demo@brainstormaikit.com',
              content: 'Hi, I\'d like to schedule a demo of your platform. When would be a good time?',
              timestamp: '2024-01-15T14:30:00Z',
              type: 'email',
              direction: 'inbound'
            }
          ]
        },
        {
          id: 2,
          contact: {
            id: 2,
            name: 'Mike Chen',
            email: 'mike@techstartup.com',
            phone: '+1 (555) 987-6543',
            avatar: null
          },
          type: 'sms',
          subject: null,
          last_message: 'Thanks for the quick response! Looking forward to our call tomorrow.',
          last_message_at: '2024-01-15T12:45:00Z',
          unread_count: 0,
          status: 'closed',
          assigned_to: 'Demo User',
          tags: ['customer', 'support'],
          ai_sentiment: 'positive',
          ai_priority: 'medium',
          messages: [
            {
              id: 4,
              from: '+15559876543',
              to: '+15551234567',
              content: 'Hi, I need help setting up the automation workflows.',
              timestamp: '2024-01-15T11:30:00Z',
              type: 'sms',
              direction: 'inbound'
            },
            {
              id: 5,
              from: '+15551234567',
              to: '+15559876543',
              content: 'I can help you with that! Let me schedule a quick call to walk you through the setup.',
              timestamp: '2024-01-15T11:45:00Z',
              type: 'sms',
              direction: 'outbound'
            },
            {
              id: 6,
              from: '+15559876543',
              to: '+15551234567',
              content: 'Thanks for the quick response! Looking forward to our call tomorrow.',
              timestamp: '2024-01-15T12:45:00Z',
              type: 'sms',
              direction: 'inbound'
            }
          ]
        },
        {
          id: 3,
          contact: {
            id: 3,
            name: 'Lisa Rodriguez',
            email: 'lisa@marketingagency.com',
            phone: '+1 (555) 456-7890',
            avatar: null
          },
          type: 'call',
          subject: 'Follow-up Call',
          last_message: 'Missed call - Left voicemail about pricing discussion',
          last_message_at: '2024-01-15T10:15:00Z',
          unread_count: 1,
          status: 'pending',
          assigned_to: 'Demo User',
          tags: ['prospect', 'pricing'],
          ai_sentiment: 'neutral',
          ai_priority: 'high',
          messages: [
            {
              id: 7,
              from: '+15554567890',
              to: '+15551234567',
              content: 'Missed call - Left voicemail about pricing discussion',
              timestamp: '2024-01-15T10:15:00Z',
              type: 'call',
              direction: 'inbound',
              call_duration: 0,
              call_status: 'missed'
            }
          ]
        }
      ])
      
      // Set first conversation as selected
      setSelectedConversation(conversations[0] || null)
    } catch (error) {
      console.error('Error fetching conversations:', error)
    } finally {
      setLoading(false)
    }
  }

  const sendMessage = async () => {
    if (!newMessage.trim() || !selectedConversation) return

    try {
      const message = {
        id: Date.now(),
        from: 'demo@brainstormaikit.com',
        to: selectedConversation.contact.email,
        content: newMessage,
        timestamp: new Date().toISOString(),
        type: selectedConversation.type,
        direction: 'outbound'
      }

      // Update conversation
      setConversations(prev => prev.map(conv => 
        conv.id === selectedConversation.id 
          ? {
              ...conv,
              messages: [...conv.messages, message],
              last_message: newMessage,
              last_message_at: message.timestamp
            }
          : conv
      ))

      // Update selected conversation
      setSelectedConversation(prev => ({
        ...prev,
        messages: [...prev.messages, message],
        last_message: newMessage,
        last_message_at: message.timestamp
      }))

      setNewMessage('')
    } catch (error) {
      console.error('Error sending message:', error)
    }
  }

  const getConversationIcon = (type) => {
    switch (type) {
      case 'email':
        return <Mail className="h-4 w-4" />
      case 'sms':
        return <MessageSquare className="h-4 w-4" />
      case 'call':
        return <Phone className="h-4 w-4" />
      default:
        return <MessageSquare className="h-4 w-4" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'open':
        return 'bg-green-100 text-green-800'
      case 'pending':
        return 'bg-yellow-100 text-yellow-800'
      case 'closed':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'text-red-600'
      case 'medium':
        return 'text-yellow-600'
      case 'low':
        return 'text-green-600'
      default:
        return 'text-gray-600'
    }
  }

  const getSentimentIcon = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return <Smile className="h-4 w-4 text-green-600" />
      case 'negative':
        return <AlertCircle className="h-4 w-4 text-red-600" />
      case 'neutral':
        return <User className="h-4 w-4 text-gray-600" />
      default:
        return <User className="h-4 w-4 text-gray-600" />
    }
  }

  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffInHours = (now - date) / (1000 * 60 * 60)
    
    if (diffInHours < 1) {
      return `${Math.floor(diffInHours * 60)}m ago`
    } else if (diffInHours < 24) {
      return `${Math.floor(diffInHours)}h ago`
    } else {
      return date.toLocaleDateString()
    }
  }

  const filteredConversations = conversations.filter(conv => {
    const matchesSearch = !searchQuery || 
      conv.contact.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      conv.last_message.toLowerCase().includes(searchQuery.toLowerCase())
    
    const matchesTab = activeTab === 'all' || conv.type === activeTab
    
    return matchesSearch && matchesTab
  })

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Communications</h1>
          <p className="text-gray-600">Unified inbox for all your customer communications</p>
        </div>
        
        <div className="flex items-center space-x-2">
          <Button variant="outline">
            <Filter className="h-4 w-4 mr-2" />
            Filter
          </Button>
          
          <Dialog open={showNewConversation} onOpenChange={setShowNewConversation}>
            <DialogTrigger asChild>
              <Button>
                <Send className="h-4 w-4 mr-2" />
                New Message
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Start New Conversation</DialogTitle>
                <DialogDescription>
                  Send a new message to a contact
                </DialogDescription>
              </DialogHeader>
              
              <div className="space-y-4 py-4">
                <div className="space-y-2">
                  <Label>Contact</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select contact" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="sarah">Sarah Johnson</SelectItem>
                      <SelectItem value="mike">Mike Chen</SelectItem>
                      <SelectItem value="lisa">Lisa Rodriguez</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="space-y-2">
                  <Label>Channel</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select channel" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="email">Email</SelectItem>
                      <SelectItem value="sms">SMS</SelectItem>
                      <SelectItem value="call">Call</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="space-y-2">
                  <Label>Message</Label>
                  <Textarea placeholder="Type your message..." rows={4} />
                </div>
              </div>
              
              <DialogFooter>
                <Button variant="outline" onClick={() => setShowNewConversation(false)}>
                  Cancel
                </Button>
                <Button>Send Message</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar - Conversations List */}
        <div className="w-96 border-r bg-gray-50 flex flex-col">
          {/* Search and Tabs */}
          <div className="p-4 space-y-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search conversations..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="all">All</TabsTrigger>
                <TabsTrigger value="email">Email</TabsTrigger>
                <TabsTrigger value="sms">SMS</TabsTrigger>
                <TabsTrigger value="call">Calls</TabsTrigger>
              </TabsList>
            </Tabs>
          </div>

          {/* Conversations List */}
          <div className="flex-1 overflow-y-auto">
            {filteredConversations.map((conversation) => (
              <div
                key={conversation.id}
                className={`p-4 border-b cursor-pointer hover:bg-white transition-colors ${
                  selectedConversation?.id === conversation.id ? 'bg-white border-l-4 border-l-blue-500' : ''
                }`}
                onClick={() => setSelectedConversation(conversation)}
              >
                <div className="flex items-start space-x-3">
                  <Avatar className="h-10 w-10">
                    <AvatarImage src={conversation.contact.avatar} />
                    <AvatarFallback>
                      {conversation.contact.name.split(' ').map(n => n[0]).join('')}
                    </AvatarFallback>
                  </Avatar>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center space-x-2">
                        <h3 className="font-medium text-sm truncate">
                          {conversation.contact.name}
                        </h3>
                        {getConversationIcon(conversation.type)}
                        {getSentimentIcon(conversation.ai_sentiment)}
                      </div>
                      <div className="flex items-center space-x-1">
                        {conversation.unread_count > 0 && (
                          <Badge variant="default" className="text-xs">
                            {conversation.unread_count}
                          </Badge>
                        )}
                        <span className="text-xs text-gray-500">
                          {formatTime(conversation.last_message_at)}
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between mb-2">
                      <Badge className={getStatusColor(conversation.status)} variant="secondary">
                        {conversation.status}
                      </Badge>
                      <div className="flex items-center space-x-1">
                        <Brain className={`h-3 w-3 ${getPriorityColor(conversation.ai_priority)}`} />
                        <span className={`text-xs ${getPriorityColor(conversation.ai_priority)}`}>
                          {conversation.ai_priority}
                        </span>
                      </div>
                    </div>
                    
                    <p className="text-sm text-gray-600 truncate mb-2">
                      {conversation.subject || conversation.last_message}
                    </p>
                    
                    <div className="flex flex-wrap gap-1">
                      {conversation.tags.slice(0, 2).map((tag) => (
                        <Badge key={tag} variant="outline" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                      {conversation.tags.length > 2 && (
                        <Badge variant="outline" className="text-xs">
                          +{conversation.tags.length - 2}
                        </Badge>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Main Content - Conversation View */}
        <div className="flex-1 flex flex-col">
          {selectedConversation ? (
            <>
              {/* Conversation Header */}
              <div className="p-4 border-b bg-white">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <Avatar className="h-12 w-12">
                      <AvatarImage src={selectedConversation.contact.avatar} />
                      <AvatarFallback>
                        {selectedConversation.contact.name.split(' ').map(n => n[0]).join('')}
                      </AvatarFallback>
                    </Avatar>
                    
                    <div>
                      <h2 className="text-xl font-semibold">
                        {selectedConversation.contact.name}
                      </h2>
                      <div className="flex items-center space-x-4 text-sm text-gray-600">
                        <span>{selectedConversation.contact.email}</span>
                        <span>{selectedConversation.contact.phone}</span>
                        <Badge className={getStatusColor(selectedConversation.status)}>
                          {selectedConversation.status}
                        </Badge>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    {selectedConversation.type === 'call' && (
                      <>
                        <Button size="sm" variant="outline">
                          <PhoneCall className="h-4 w-4 mr-2" />
                          Call
                        </Button>
                        <Button size="sm" variant="outline">
                          <Video className="h-4 w-4 mr-2" />
                          Video
                        </Button>
                      </>
                    )}
                    
                    <Button size="sm" variant="outline">
                      <Calendar className="h-4 w-4 mr-2" />
                      Schedule
                    </Button>
                    
                    <Button size="sm" variant="outline">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                
                {/* AI Insights */}
                <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                  <div className="flex items-center mb-2">
                    <Brain className="h-4 w-4 text-blue-600 mr-2" />
                    <span className="text-sm font-medium text-blue-800">AI Insights</span>
                  </div>
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div>
                      <span className="text-blue-700">Sentiment:</span>
                      <span className="ml-2 font-medium capitalize">{selectedConversation.ai_sentiment}</span>
                    </div>
                    <div>
                      <span className="text-blue-700">Priority:</span>
                      <span className="ml-2 font-medium capitalize">{selectedConversation.ai_priority}</span>
                    </div>
                    <div>
                      <span className="text-blue-700">Intent:</span>
                      <span className="ml-2 font-medium">Product Demo</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {selectedConversation.messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.direction === 'outbound' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                        message.direction === 'outbound'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      <p className="text-sm">{message.content}</p>
                      <p className={`text-xs mt-1 ${
                        message.direction === 'outbound' ? 'text-blue-100' : 'text-gray-500'
                      }`}>
                        {formatTime(message.timestamp)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Message Input */}
              <div className="p-4 border-t bg-white">
                <div className="flex items-end space-x-2">
                  <div className="flex-1">
                    <Textarea
                      placeholder="Type your message..."
                      value={newMessage}
                      onChange={(e) => setNewMessage(e.target.value)}
                      rows={3}
                      className="resize-none"
                      onKeyPress={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                          e.preventDefault()
                          sendMessage()
                        }
                      }}
                    />
                  </div>
                  
                  <div className="flex flex-col space-y-2">
                    <Button size="sm" variant="outline">
                      <Paperclip className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="outline">
                      <Smile className="h-4 w-4" />
                    </Button>
                    <Button onClick={sendMessage} disabled={!newMessage.trim()}>
                      <Send className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                
                {/* AI Suggestions */}
                <div className="mt-3 flex flex-wrap gap-2">
                  <Button size="sm" variant="outline" className="text-xs">
                    <Zap className="h-3 w-3 mr-1" />
                    Schedule demo
                  </Button>
                  <Button size="sm" variant="outline" className="text-xs">
                    <Brain className="h-3 w-3 mr-1" />
                    Send pricing info
                  </Button>
                  <Button size="sm" variant="outline" className="text-xs">
                    <TrendingUp className="h-3 w-3 mr-1" />
                    Share case study
                  </Button>
                </div>
              </div>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <div className="text-center">
                <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Select a conversation
                </h3>
                <p className="text-gray-600">
                  Choose a conversation from the sidebar to start messaging
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

