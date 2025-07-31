import { useState } from 'react'
import { 
  Server, 
  Monitor, 
  Smartphone, 
  Database, 
  Cloud, 
  Plus,
  Search,
  Filter,
  MoreHorizontal,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Edit,
  Trash2,
  Eye
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
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Progress } from '@/components/ui/progress'

const AssetManagement = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedStatus, setSelectedStatus] = useState('all')

  // Sample asset data
  const assets = [
    {
      id: 1,
      name: 'Web Server 01',
      type: 'server',
      category: 'Infrastructure',
      ip: '192.168.1.10',
      os: 'Ubuntu 22.04',
      status: 'active',
      health: 95,
      vulnerabilities: 2,
      lastScan: '2024-01-26T10:30:00Z',
      owner: 'IT Team',
      location: 'Data Center A'
    },
    {
      id: 2,
      name: 'Database Server',
      type: 'database',
      category: 'Infrastructure',
      ip: '192.168.1.20',
      os: 'CentOS 8',
      status: 'active',
      health: 88,
      vulnerabilities: 5,
      lastScan: '2024-01-26T09:15:00Z',
      owner: 'Database Team',
      location: 'Data Center A'
    },
    {
      id: 3,
      name: 'Employee Workstation',
      type: 'workstation',
      category: 'Endpoint',
      ip: '192.168.2.45',
      os: 'Windows 11',
      status: 'active',
      health: 92,
      vulnerabilities: 1,
      lastScan: '2024-01-26T08:45:00Z',
      owner: 'John Doe',
      location: 'Office Floor 2'
    },
    {
      id: 4,
      name: 'Network Router',
      type: 'network',
      category: 'Network',
      ip: '192.168.1.1',
      os: 'RouterOS 7.1',
      status: 'warning',
      health: 78,
      vulnerabilities: 8,
      lastScan: '2024-01-26T07:30:00Z',
      owner: 'Network Team',
      location: 'Network Closet'
    },
    {
      id: 5,
      name: 'Mobile Device',
      type: 'mobile',
      category: 'Endpoint',
      ip: '192.168.3.100',
      os: 'iOS 17.2',
      status: 'active',
      health: 96,
      vulnerabilities: 0,
      lastScan: '2024-01-26T11:00:00Z',
      owner: 'Jane Smith',
      location: 'Remote'
    },
    {
      id: 6,
      name: 'Legacy System',
      type: 'server',
      category: 'Infrastructure',
      ip: '192.168.1.50',
      os: 'Windows Server 2012',
      status: 'critical',
      health: 45,
      vulnerabilities: 15,
      lastScan: '2024-01-25T16:20:00Z',
      owner: 'Legacy Team',
      location: 'Data Center B'
    }
  ]

  const getAssetIcon = (type) => {
    switch (type) {
      case 'server': return <Server className="h-5 w-5" />
      case 'workstation': return <Monitor className="h-5 w-5" />
      case 'mobile': return <Smartphone className="h-5 w-5" />
      case 'database': return <Database className="h-5 w-5" />
      case 'network': return <Cloud className="h-5 w-5" />
      default: return <Server className="h-5 w-5" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100'
      case 'warning': return 'text-yellow-600 bg-yellow-100'
      case 'critical': return 'text-red-600 bg-red-100'
      case 'inactive': return 'text-gray-600 bg-gray-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getHealthColor = (health) => {
    if (health >= 90) return 'text-green-600'
    if (health >= 70) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getVulnerabilityColor = (count) => {
    if (count === 0) return 'text-green-600 bg-green-100'
    if (count <= 3) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString()
  }

  const filteredAssets = assets.filter(asset => {
    const matchesSearch = asset.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         asset.ip.includes(searchQuery) ||
                         asset.owner.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = selectedCategory === 'all' || asset.category.toLowerCase() === selectedCategory
    const matchesStatus = selectedStatus === 'all' || asset.status === selectedStatus
    
    return matchesSearch && matchesCategory && matchesStatus
  })

  // Asset statistics
  const totalAssets = assets.length
  const activeAssets = assets.filter(a => a.status === 'active').length
  const criticalAssets = assets.filter(a => a.status === 'critical').length
  const totalVulnerabilities = assets.reduce((sum, asset) => sum + asset.vulnerabilities, 0)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Asset Management</h1>
          <p className="text-gray-600 dark:text-gray-400">Monitor and manage your IT infrastructure</p>
        </div>
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          Add Asset
        </Button>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Assets</CardTitle>
            <Server className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">{totalAssets}</div>
            <p className="text-xs text-muted-foreground">Across all categories</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Assets</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{activeAssets}</div>
            <p className="text-xs text-muted-foreground">{Math.round((activeAssets/totalAssets)*100)}% of total</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical Assets</CardTitle>
            <XCircle className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{criticalAssets}</div>
            <p className="text-xs text-muted-foreground">Require immediate attention</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Vulnerabilities</CardTitle>
            <AlertTriangle className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">{totalVulnerabilities}</div>
            <p className="text-xs text-muted-foreground">Across all assets</p>
          </CardContent>
        </Card>
      </div>

      {/* Search and Filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search assets by name, IP, or owner..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger className="w-40">
                  <SelectValue placeholder="Category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  <SelectItem value="infrastructure">Infrastructure</SelectItem>
                  <SelectItem value="endpoint">Endpoint</SelectItem>
                  <SelectItem value="network">Network</SelectItem>
                </SelectContent>
              </Select>
              <Select value={selectedStatus} onValueChange={setSelectedStatus}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="active">Active</SelectItem>
                  <SelectItem value="warning">Warning</SelectItem>
                  <SelectItem value="critical">Critical</SelectItem>
                  <SelectItem value="inactive">Inactive</SelectItem>
                </SelectContent>
              </Select>
              <Button variant="outline">
                <Filter className="w-4 h-4 mr-2" />
                More Filters
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Assets Table */}
      <Card>
        <CardHeader>
          <CardTitle>Assets ({filteredAssets.length})</CardTitle>
          <CardDescription>Detailed view of all managed assets</CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Asset</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Health</TableHead>
                <TableHead>Vulnerabilities</TableHead>
                <TableHead>Last Scan</TableHead>
                <TableHead>Owner</TableHead>
                <TableHead>Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredAssets.map((asset) => (
                <TableRow key={asset.id}>
                  <TableCell>
                    <div className="flex items-center space-x-3">
                      {getAssetIcon(asset.type)}
                      <div>
                        <p className="font-medium">{asset.name}</p>
                        <p className="text-sm text-gray-500">{asset.ip}</p>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <div>
                      <p className="font-medium capitalize">{asset.type}</p>
                      <p className="text-sm text-gray-500">{asset.os}</p>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge className={getStatusColor(asset.status)}>
                      {asset.status}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <div className="flex items-center space-x-2">
                      <Progress value={asset.health} className="w-16" />
                      <span className={`text-sm font-medium ${getHealthColor(asset.health)}`}>
                        {asset.health}%
                      </span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge className={getVulnerabilityColor(asset.vulnerabilities)}>
                      {asset.vulnerabilities}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <span className="text-sm text-gray-500">
                      {formatDate(asset.lastScan)}
                    </span>
                  </TableCell>
                  <TableCell>
                    <div>
                      <p className="font-medium">{asset.owner}</p>
                      <p className="text-sm text-gray-500">{asset.location}</p>
                    </div>
                  </TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuItem>
                          <Eye className="mr-2 h-4 w-4" />
                          View Details
                        </DropdownMenuItem>
                        <DropdownMenuItem>
                          <Edit className="mr-2 h-4 w-4" />
                          Edit Asset
                        </DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem className="text-red-600">
                          <Trash2 className="mr-2 h-4 w-4" />
                          Delete Asset
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Asset Categories Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Infrastructure Assets</CardTitle>
            <CardDescription>Servers, databases, and core systems</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {assets.filter(a => a.category === 'Infrastructure').map(asset => (
                <div key={asset.id} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    {getAssetIcon(asset.type)}
                    <span className="text-sm">{asset.name}</span>
                  </div>
                  <Badge className={getStatusColor(asset.status)} variant="secondary">
                    {asset.status}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Endpoint Assets</CardTitle>
            <CardDescription>Workstations and mobile devices</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {assets.filter(a => a.category === 'Endpoint').map(asset => (
                <div key={asset.id} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    {getAssetIcon(asset.type)}
                    <span className="text-sm">{asset.name}</span>
                  </div>
                  <Badge className={getStatusColor(asset.status)} variant="secondary">
                    {asset.status}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Network Assets</CardTitle>
            <CardDescription>Routers, switches, and network devices</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {assets.filter(a => a.category === 'Network').map(asset => (
                <div key={asset.id} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    {getAssetIcon(asset.type)}
                    <span className="text-sm">{asset.name}</span>
                  </div>
                  <Badge className={getStatusColor(asset.status)} variant="secondary">
                    {asset.status}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default AssetManagement

