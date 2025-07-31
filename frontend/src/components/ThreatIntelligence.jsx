import { useState, useEffect } from 'react'
import { 
  Search, 
  AlertTriangle, 
  Eye, 
  Download, 
  Filter,
  Globe,
  Mail,
  Hash,
  Calendar,
  TrendingUp,
  Shield,
  Database
} from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar
} from 'recharts'

const ThreatIntelligence = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedTimeRange, setSelectedTimeRange] = useState('7d')

  // Sample data for leaked credentials
  const leakedCredentials = [
    {
      id: 1,
      email: 'john.doe@quantashield.in',
      domain: 'quantashield.in',
      source: 'RedLine Stealer',
      discovered: '2024-01-26T10:30:00Z',
      severity: 'high',
      breach: 'Corporate Data Leak 2024'
    },
    {
      id: 2,
      email: 'admin@quantashield.in',
      domain: 'quantashield.in',
      source: 'Raccoon Stealer',
      discovered: '2024-01-25T15:45:00Z',
      severity: 'critical',
      breach: 'Admin Panel Compromise'
    },
    {
      id: 3,
      email: 'support@quantashield.in',
      domain: 'quantashield.in',
      source: 'Meta Stealer',
      discovered: '2024-01-24T09:15:00Z',
      severity: 'medium',
      breach: 'Support System Breach'
    },
    {
      id: 4,
      email: 'sales@quantashield.in',
      domain: 'quantashield.in',
      source: 'Telegram Channel',
      discovered: '2024-01-23T14:20:00Z',
      severity: 'high',
      breach: 'Sales Database Leak'
    }
  ]

  // Sample data for threat indicators
  const threatIndicators = [
    {
      id: 1,
      type: 'ip',
      value: '192.168.1.100',
      threat_type: 'malware',
      confidence: 95,
      first_seen: '2024-01-20T08:00:00Z',
      last_seen: '2024-01-26T12:00:00Z',
      tags: ['botnet', 'c2-server']
    },
    {
      id: 2,
      type: 'domain',
      value: 'malicious-site.example',
      threat_type: 'phishing',
      confidence: 88,
      first_seen: '2024-01-22T10:30:00Z',
      last_seen: '2024-01-26T11:45:00Z',
      tags: ['phishing', 'credential-theft']
    },
    {
      id: 3,
      type: 'hash',
      value: 'a1b2c3d4e5f6...',
      threat_type: 'malware',
      confidence: 92,
      first_seen: '2024-01-21T14:15:00Z',
      last_seen: '2024-01-26T09:30:00Z',
      tags: ['trojan', 'data-exfil']
    }
  ]

  // Sample data for underground sources
  const undergroundSources = [
    { name: 'Telegram Channel Alpha', status: 'active', last_update: '5 min ago', credentials: 1247 },
    { name: 'Dark Web Forum Beta', status: 'active', last_update: '12 min ago', credentials: 892 },
    { name: 'Underground Market Gamma', status: 'monitoring', last_update: '1 hour ago', credentials: 2156 },
    { name: 'Stealer Log Delta', status: 'active', last_update: '3 min ago', credentials: 567 }
  ]

  // Sample data for trends
  const credentialTrends = [
    { date: '2024-01-20', count: 45 },
    { date: '2024-01-21', count: 67 },
    { date: '2024-01-22', count: 89 },
    { date: '2024-01-23', count: 123 },
    { date: '2024-01-24', count: 156 },
    { date: '2024-01-25', count: 134 },
    { date: '2024-01-26', count: 178 }
  ]

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'bg-red-500 text-white'
      case 'high': return 'bg-orange-500 text-white'
      case 'medium': return 'bg-yellow-500 text-black'
      case 'low': return 'bg-green-500 text-white'
      default: return 'bg-gray-500 text-white'
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100'
      case 'monitoring': return 'text-yellow-600 bg-yellow-100'
      case 'inactive': return 'text-gray-600 bg-gray-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString()
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Threat Intelligence</h1>
          <p className="text-gray-600 dark:text-gray-400">Underground log intelligence and threat monitoring</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant="outline" className="text-blue-600 border-blue-600">
            <Database className="w-3 h-3 mr-1" />
            50+ Sources Active
          </Badge>
        </div>
      </div>

      {/* Search and Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search by email, domain, IP, or hash..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <Select value={selectedTimeRange} onValueChange={setSelectedTimeRange}>
                <SelectTrigger className="w-32">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1d">Last 24h</SelectItem>
                  <SelectItem value="7d">Last 7 days</SelectItem>
                  <SelectItem value="30d">Last 30 days</SelectItem>
                  <SelectItem value="90d">Last 90 days</SelectItem>
                </SelectContent>
              </Select>
              <Button variant="outline">
                <Filter className="w-4 h-4 mr-2" />
                Filters
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Credentials</CardTitle>
            <Mail className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">265,847</div>
            <p className="text-xs text-muted-foreground">+1,234 in last 24h</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Unique Domains</CardTitle>
            <Globe className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">250,000</div>
            <p className="text-xs text-muted-foreground">Monitored domains</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Threats</CardTitle>
            <AlertTriangle className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">1,847</div>
            <p className="text-xs text-muted-foreground">High confidence IOCs</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Sources Online</CardTitle>
            <Shield className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">52/54</div>
            <p className="text-xs text-muted-foreground">96% uptime</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs defaultValue="credentials" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="credentials">Leaked Credentials</TabsTrigger>
          <TabsTrigger value="indicators">Threat Indicators</TabsTrigger>
          <TabsTrigger value="sources">Underground Sources</TabsTrigger>
          <TabsTrigger value="trends">Trends & Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="credentials" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Recent Credential Leaks</CardTitle>
              <CardDescription>Latest credentials discovered from underground sources</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {leakedCredentials.map((cred) => (
                  <div key={cred.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                    <div className="flex items-center space-x-4">
                      <Mail className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="font-medium">{cred.email}</p>
                        <p className="text-sm text-gray-500">
                          Source: {cred.source} • {formatDate(cred.discovered)}
                        </p>
                        <p className="text-xs text-gray-400">{cred.breach}</p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge className={getSeverityColor(cred.severity)}>
                        {cred.severity}
                      </Badge>
                      <Button variant="outline" size="sm">
                        <Eye className="w-4 h-4 mr-1" />
                        Details
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex justify-center mt-6">
                <Button variant="outline">
                  <Download className="w-4 h-4 mr-2" />
                  Export Results
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="indicators" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Threat Indicators</CardTitle>
              <CardDescription>IOCs from various threat intelligence sources</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {threatIndicators.map((indicator) => (
                  <div key={indicator.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                    <div className="flex items-center space-x-4">
                      {indicator.type === 'ip' && <Globe className="h-5 w-5 text-blue-400" />}
                      {indicator.type === 'domain' && <Globe className="h-5 w-5 text-green-400" />}
                      {indicator.type === 'hash' && <Hash className="h-5 w-5 text-purple-400" />}
                      <div>
                        <p className="font-medium font-mono">{indicator.value}</p>
                        <p className="text-sm text-gray-500">
                          Type: {indicator.type} • Threat: {indicator.threat_type}
                        </p>
                        <div className="flex space-x-1 mt-1">
                          {indicator.tags.map((tag, index) => (
                            <Badge key={index} variant="secondary" className="text-xs">
                              {tag}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="text-right">
                        <p className="text-sm font-medium">Confidence: {indicator.confidence}%</p>
                        <p className="text-xs text-gray-500">
                          Last seen: {formatDate(indicator.last_seen)}
                        </p>
                      </div>
                      <Button variant="outline" size="sm">
                        <Eye className="w-4 h-4 mr-1" />
                        Analyze
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="sources" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Underground Intelligence Sources</CardTitle>
              <CardDescription>Status of dark web and underground monitoring sources</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {undergroundSources.map((source, index) => (
                  <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center space-x-4">
                      <Database className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="font-medium">{source.name}</p>
                        <p className="text-sm text-gray-500">
                          Last update: {source.last_update}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <p className="text-sm font-medium">{source.credentials.toLocaleString()} credentials</p>
                        <Badge className={getStatusColor(source.status)}>
                          {source.status}
                        </Badge>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="trends" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Credential Discovery Trends</CardTitle>
                <CardDescription>Daily credential discovery volume</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={credentialTrends}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="date" 
                      tickFormatter={(value) => new Date(value).toLocaleDateString()}
                    />
                    <YAxis />
                    <Tooltip 
                      labelFormatter={(value) => new Date(value).toLocaleDateString()}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="count" 
                      stroke="#ef4444" 
                      strokeWidth={2}
                      name="Credentials Found"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Top Affected Domains</CardTitle>
                <CardDescription>Domains with most leaked credentials</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={[
                    { domain: 'quantashield.in', count: 45 },
                    { domain: 'example.org', count: 32 },
                    { domain: 'business.net', count: 28 },
                    { domain: 'enterprise.io', count: 24 },
                    { domain: 'startup.co', count: 19 }
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="domain" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#ef4444" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default ThreatIntelligence

