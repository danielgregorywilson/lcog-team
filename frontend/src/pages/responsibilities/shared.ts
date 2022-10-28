import { Responsibility } from '../../store/types'


export default {
    tableFilterMethod(rows: Array<Responsibility>, term: string, filterOn: Array<'name'|'description'|'tags'>) {
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
                if (filterOn.indexOf('name') != -1) {
                    const nameMatches = row.name.toLowerCase().includes(searchTerm)
                    matchCriteria.push(nameMatches)
                }
                if (filterOn.indexOf('description') != -1) {
                    const descriptionMatches = row.description.toLowerCase().includes(searchTerm)
                    matchCriteria.push(descriptionMatches)
                }
                if (filterOn.indexOf('tags') != -1) {
                    let tagsMatch = false
                    for (let i=0; i<row.tags.length; i++) {
                        if (row.tags[i].name.toLowerCase().includes(searchTerm)) {
                            tagsMatch = true
                        }
                    }
                    matchCriteria.push(tagsMatch)
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