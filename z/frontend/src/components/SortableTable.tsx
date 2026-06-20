import { useState } from 'react'

interface SortableTableProps {
  children: React.ReactNode
  pageSize?: number
}

type SortDirection = 'asc' | 'desc' | null

export default function SortableTable({ children, pageSize = 10 }: SortableTableProps) {
  const [sortColumn, setSortColumn] = useState<number | null>(null)
  const [sortDirection, setSortDirection] = useState<SortDirection>(null)
  const [currentPage, setCurrentPage] = useState(1)

  // Extract thead and tbody from children
  const childArray = Array.isArray(children) ? children : [children]
  const thead = childArray.find((child: any) => child?.type === 'thead')
  const tbody = childArray.find((child: any) => child?.type === 'tbody')

  if (!thead || !tbody) {
    return <table>{children}</table>
  }

  // Extract headers
  const headerRow = thead.props.children
  const headers = Array.isArray(headerRow?.props?.children)
    ? headerRow.props.children
    : [headerRow?.props?.children]

  // Extract rows
  const rows = Array.isArray(tbody.props.children)
    ? tbody.props.children.filter((child: any) => child)
    : [tbody.props.children].filter((child: any) => child)

  const handleHeaderClick = (columnIndex: number) => {
    // Reset to page 1 when sorting changes
    setCurrentPage(1)

    if (sortColumn === columnIndex) {
      // Cycle through: asc -> desc -> null
      if (sortDirection === 'asc') {
        setSortDirection('desc')
      } else if (sortDirection === 'desc') {
        setSortDirection(null)
        setSortColumn(null)
      }
    } else {
      setSortColumn(columnIndex)
      setSortDirection('asc')
    }
  }

  // Sort rows if a column is selected
  let sortedRows = [...rows]
  if (sortColumn !== null && sortDirection !== null) {
    sortedRows.sort((a: any, b: any) => {
      const aCells = Array.isArray(a.props.children) ? a.props.children : [a.props.children]
      const bCells = Array.isArray(b.props.children) ? b.props.children : [b.props.children]

      const aCell = aCells[sortColumn]
      const bCell = bCells[sortColumn]

      // Get text content from cells
      const aText = getCellText(aCell)
      const bText = getCellText(bCell)

      // Try to parse as numbers
      const aNum = parseFloat(aText)
      const bNum = parseFloat(bText)

      let comparison = 0
      if (!isNaN(aNum) && !isNaN(bNum)) {
        // Numeric comparison
        comparison = aNum - bNum
      } else {
        // String comparison
        comparison = aText.localeCompare(bText, undefined, { numeric: true, sensitivity: 'base' })
      }

      return sortDirection === 'asc' ? comparison : -comparison
    })
  }

  // Calculate pagination
  const totalRows = sortedRows.length
  const totalPages = Math.ceil(totalRows / pageSize)
  const showPagination = totalRows > pageSize

  // Get current page rows
  const startIndex = (currentPage - 1) * pageSize
  const endIndex = startIndex + pageSize
  const currentRows = sortedRows.slice(startIndex, endIndex)

  const handlePageChange = (page: number) => {
    setCurrentPage(page)
  }

  const handlePrevious = () => {
    if (currentPage > 1) setCurrentPage(currentPage - 1)
  }

  const handleNext = () => {
    if (currentPage < totalPages) setCurrentPage(currentPage + 1)
  }

  // Generate page numbers to show
  const getPageNumbers = () => {
    const pages: (number | string)[] = []
    const maxVisible = 5

    if (totalPages <= maxVisible) {
      // Show all pages
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i)
      }
    } else {
      // Show first, last, and pages around current
      pages.push(1)

      if (currentPage > 3) {
        pages.push('...')
      }

      for (let i = Math.max(2, currentPage - 1); i <= Math.min(totalPages - 1, currentPage + 1); i++) {
        pages.push(i)
      }

      if (currentPage < totalPages - 2) {
        pages.push('...')
      }

      pages.push(totalPages)
    }

    return pages
  }

  return (
    <div className="sortable-table-container">
      <table>
        <thead>
          <tr>
            {headers.map((header: any, index: number) => (
              <th
                key={index}
                onClick={() => handleHeaderClick(index)}
                className={`sortable-header ${sortColumn === index ? 'sorted' : ''}`}
                style={{ cursor: 'pointer', userSelect: 'none' }}
              >
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '8px' }}>
                  <span>{header?.props?.children || header}</span>
                  <span className="sort-indicator">
                    {sortColumn === index && sortDirection === 'asc' && '↑'}
                    {sortColumn === index && sortDirection === 'desc' && '↓'}
                    {sortColumn !== index && '↕'}
                  </span>
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {currentRows.map((row: any, index: number) => (
            <tr key={index}>{row.props.children}</tr>
          ))}
        </tbody>
      </table>

      {showPagination && (
        <div className="table-pagination">
          <div className="pagination-info">
            Showing {startIndex + 1}-{Math.min(endIndex, totalRows)} of {totalRows} rows
          </div>
          <div className="pagination-controls">
            <button
              className="pagination-button"
              onClick={handlePrevious}
              disabled={currentPage === 1}
            >
              Previous
            </button>

            {getPageNumbers().map((page, index) => (
              typeof page === 'number' ? (
                <button
                  key={index}
                  className={`pagination-button ${currentPage === page ? 'active' : ''}`}
                  onClick={() => handlePageChange(page)}
                >
                  {page}
                </button>
              ) : (
                <span key={index} className="pagination-ellipsis">{page}</span>
              )
            ))}

            <button
              className="pagination-button"
              onClick={handleNext}
              disabled={currentPage === totalPages}
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

// Helper function to extract text from cell
function getCellText(cell: any): string {
  if (!cell) return ''
  if (typeof cell === 'string') return cell
  if (typeof cell === 'number') return String(cell)
  if (cell.props?.children) {
    if (typeof cell.props.children === 'string') return cell.props.children
    if (Array.isArray(cell.props.children)) {
      return cell.props.children.map((c: any) => getCellText(c)).join('')
    }
    return getCellText(cell.props.children)
  }
  return ''
}
