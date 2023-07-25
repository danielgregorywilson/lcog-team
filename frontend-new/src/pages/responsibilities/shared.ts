import { Responsibility } from 'src/types'


export default {
  tableFilterMethod(
    rows: Array<Responsibility>,
    term: string,
    filterOn: Array<'name'|'description'|'link'|'tags'|'primaryEmployee'|'secondaryEmployee'>
  ): Array<Responsibility> {
      // rows contain the entire data
      // terms contains whatever you have as filter
  
      const searchTerm = term ? term.toLowerCase() : ''
  
      const filteredRows = rows.filter(
        (row) =>{
          if (searchTerm == '') {
              // If no search term, return all rows
              return true
          } else {
              // Check columns that were requested
              const matchCriteria: Array<boolean> = []
              if (filterOn.includes('name')) {
                  const nameMatches = row.name.toLowerCase().includes(searchTerm)
                  matchCriteria.push(nameMatches)
              }
              if (filterOn.includes('description')) {
                  const descriptionMatches = row.description.toLowerCase().includes(searchTerm)
                  matchCriteria.push(descriptionMatches)
              }
              if (filterOn.includes('link')) {
                  const linkMatches = row.link.toLowerCase().includes(searchTerm)
                  matchCriteria.push(linkMatches)
              }
              if (filterOn.includes('tags')) {
                  let tagsMatch = false
                  for (let i=0; i<row.tags.length; i++) {
                      if (row.tags[i].name.toLowerCase().includes(searchTerm)) {
                          tagsMatch = true
                      }
                  }
                  matchCriteria.push(tagsMatch)
              }
              if (filterOn.includes('primaryEmployee')) {
                  let primaryEmployeeMatches = false
                  if (row.primary_employee_name) {
                      primaryEmployeeMatches = row.primary_employee_name.toLowerCase().includes(searchTerm)
                  }
                  matchCriteria.push(primaryEmployeeMatches)
              }
              if (filterOn.includes('secondaryEmployee')) {
                  let secondaryEmployeeMatches = false
                  if (row.secondary_employee_name) {
                      secondaryEmployeeMatches = row.secondary_employee_name.toLowerCase().includes(searchTerm)
                  }
                  matchCriteria.push(secondaryEmployeeMatches)
              }
              if (matchCriteria.some(c => !!c)) {
                  return true
              }
              // Assume row doesn't match
              return false
          }
        })
      return filteredRows
    }
  }