// ////////////////////////////////
// WATCH THOSE MONTH CODES, NOOB //
///////////////////////////////////

export const releases = [
  {
    version: '0.4.9',
    date: new Date(2022, 5, 8),
    changes: [
      {
        type: 'improved',
        description: 'Security upgrades.'
      }
    ]
  },
  {
    version: '0.4.8',
    date: new Date(2022, 4, 16),
    changes: [
      {
        type: 'improved',
        description: 'Add a screensaver at night to the desk reservation screens.'
      },
      {
        type: 'improved',
        description: 'Update Schaefers floor plans.'
      },
      {
        type: 'improved',
        description: 'Allow employees to be archived.'
      }
    ]
  },
  {
    version: '0.4.7',
    date: new Date(2022, 4, 9),
    changes: [
      {
        type: 'improved',
        description: 'Simplify desk reservation header.'
      }
    ]
  },
  {
    version: '0.4.6',
    date: new Date(2022, 4, 2),
    changes: [
      {
        type: 'new',
        description: 'Add a staging site for testing new features.'
      }
    ]
  },
  {
    version: '0.4.5',
    date: new Date(2022, 3, 30),
    changes: [
      {
        type: 'fix',
        description: 'Fix a bug where desks don\'t display on weekends.'
      }
    ]
  },
  {
    version: '0.4.4',
    date: new Date(2022, 3, 27),
    changes: [
      {
        type: 'improved',
        description: 'Desks can now have weekly holds placed on them for certain employees.'
      },
      {
        type: 'improved',
        description: 'Desk reservation app now blocked unless you are authenticated or on a trusted IP.'
      }
    ]
  },
  {
    version: '0.4.3',
    date: new Date(2022, 3, 22),
    changes: [
      {
        type: 'improved',
        description: 'Update floor plans processing code to be compatible with new Illustrator version changes.'
      },
      {
        type: 'improved',
        description: 'Desks can now be deactivated.'
      }
    ]
  },
  {
    version: '0.4.2',
    date: new Date(2022, 3, 19),
    changes: [
      {
        type: 'improved',
        description: 'Adjust desk reservation app to fit better on office laptop screens.'
      }
    ]
  },
  {
    version: '0.4.1',
    date: new Date(2022, 3, 18),
    changes: [
      {
        type: 'new',
        description: 'Add Desk Reservation reports.'
      },
      {
        type: 'improved',
        description: 'Responsibility app looks better on smaller screens.'
      }
    ]
  },
  {
    version: '0.4.0',
    date: new Date(2022, 3, 11),
    changes: [
      {
        type: 'improved',
        description: 'Migrate desk reservation data to a new Django app.'
      }
    ]
  },
  {
    version: '0.3.4',
    date: new Date(2022, 3, 8),
    changes: [
      {
        type: 'improved',
        description: 'End all active desk reservations every day at 7 PM.'
      }
    ]
  },
  {
    version: '0.3.3',
    date: new Date(2022, 3, 7),
    changes: [
      {
        type: 'improved',
        description: 'Add end time, rather than delete, desk reservations upon check out.'
      },
      {
        type: 'improved',
        description: 'Prevent double booking of desk reservations by canceling existing reservations when a new one is made.'
      }
    ]
  },
  {
    version: '0.3.2',
    date: new Date(2022, 2, 18),
    changes: [
      {
        type: 'improved',
        description: 'Added second and third Schaefers floors to desk reservation app'
      },
      {
        type: 'improved',
        description: 'Cleaned up desk reservation app layout'
      }
    ]
  },
  {
    version: '0.3.1',
    date: new Date(2022, 2, 9),
    changes: [
      {
        type: 'new',
        description: 'Responsibilities can be tagged'
      },
      {
        type: 'new',
        description: 'Responsibilities now have descriptions and links'
      },
      {
        type: 'new',
        description: 'View all responsibilities by tag'
      },
      {
        type: 'new',
        description: 'Filter all responsibility tables by name, description, and tag'
      },
      {
        type: 'improved',
        description: 'Responsibility app UI improvements'
      }
    ]
  },
  {
    version: '0.3.0',
    date: new Date(2022, 2, 7),
    changes: [
      {
        type: 'improved',
        description: 'Update desk reservation app UI significantly'
      },
      {
        type: 'improved',
        description: 'Migrate responsibility app data to its own Django app'
      }
    ]
  },
  {
    version: '0.2.2',
    date: new Date(2022, 1, 22),
    changes: [
      {
        type: 'new',
        description: 'Demo of mileage reimbursement app'
      }
    ]
  },
  {
    version: '0.2.1',
    date: new Date(2022, 1, 8),
    changes: [
      {
        type: 'new',
        description: 'Demo of desk reservation app'
      }
    ]
  },
  {
    version: '0.2.0',
    date: new Date(2022, 0, 14),
    changes: [
      {
        type: 'improved',
        description: 'Upgrade to Django 4'
      }
    ]
  },
  {
    version: '0.1.4',
    date: new Date(2021, 9, 29),
    changes: [
      {
        type: 'improved',
        description: 'Responsibilities module: filter employee list dropdown by typing'
      }
    ]
  },
  {
    version: '0.1.3',
    date: new Date(2021, 9, 26),
    changes: [
      {
        type: 'new',
        description: 'Responsibilities Module'
      },
      {
        type: 'new',
        description: 'Release Notes page'
      },
      {
        type: 'improved',
        description: 'Add LCOG logo to menu'
      },
      {
        type: 'improved',
        description: 'Add Schaefers 2nd and 3rd floor plans to seating chart'
      }
    ]
  },
  {
    version: '0.1.2',
    date: new Date(2021, 9, 11),
    changes: [
      {
        type: 'new',
        description: 'Seating chart demo'
      }
    ]
  },
  {
    version: '0.1.1',
    date: new Date(2021, 9, 7),
    changes: [
      {
        type: 'new',
        description: 'Add seating chart demo page'
      },
      {
        type: 'improved',
        description: 'Admin: Add user inline to group detail'
      }
    ]
  },
  {
    version: '0.1.0',
    date: new Date(2021, 9, 5),
    changes: [
      {
        type: 'new',
        description: 'Add app version to header'
      },
      {
        type: 'improved',
        description: 'Clean up navigation'
      }
    ]
  }
]