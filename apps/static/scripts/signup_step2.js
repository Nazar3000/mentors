const step2Form = new Vue({
  el: '#step2-form',
  delimiters: ['[[', ']]'],
  data: {
    choices: {
      able_to_visit_child_frequency: {},
      education_types: {},
      genders: {},
      home_types: {},
      local_church_visiting_frequency: {},
      marital_statuses: {},
      mentoring_program_find_out_places: {},
      religions: {},
    },

    full_name: '',
    date_of_birth: '',
    phone_number: '',
    email: '',
    nationality: '',
    actual_address: '',
    registration_address: '',
    religion: '',
    local_church_visiting: '',
    local_church_visiting_frequency: '',
    health_self_estimation: '',
    serious_diseases: '',
    narcologist: '',
    psychiatrist: '',
    phthisiatrician: '',
    therapist: '',
    dermatovenereologist: '',
    hospital_data: '',
    hiv_infected: '',
    interests_and_hobbies: '',
    marital_status: '',
    home_type: '',
    room_count: '',
    people_per_room: '',
    home_family_members_data: '',
    pets_data: '',
    join_reason: '',
    helpful_specifics: '',
    self_char: '',
    want_to_help_reason: '',
    expectations_from_child: '',
    socialization: '',
    proforientation: '',
    help_in_education: '',
    able_to_visit_frequency: '',
    ready_for_child_with_disabilities: '',
    drink_alcohol: '',
    drink_alcohol_frequency: '',
    smoke_cigarettes: '',
    psychotropic_substances: '',
    psychotropic_substances_names: '',
    drug_usage: '',
    drug_usage_info: '',
    crime_convicted: '',
    crime_convicted_description: '',
    parental_rights_deprived: '',
    parental_rights_deprived_description: '',
    allow_to_use_personal_data: '',
    program_found_out_place: '',
    convenient_meeting_conditions: '',

    educations: [
      {
        education_type: '',
        year_of_admission: '',
        year_of_graduation: '',
        degree: ''
      },
    ],
    jobs: [
      {
        is_current: true,
        organization_name: '',
        date_since: '',
        date_till: '',
        contact_info: '',
        position: '',
        duties: '',
        reason_for_leaving: ''
      },
      {
        is_current: false,
        organization_name: '',
        date_since: '',
        date_till: '',
        contact_info: '',
        position: '',
        duties: '',
        reason_for_leaving: ''
      },
    ],
    family_members: [
      {
        name: '',
        gender: '',
        date_of_birth: '',
        relation: ''
      }
    ],
    children_work_experiences: [
      {
        organization_name: '',
        date_since: '',
        date_till: '',
        contact_info: '',
        position: '',
        duties: '',
        children_age_group: ''
      },
    ],

    errors: {
      educations: [
        {},
        {},
        {}
      ],
      jobs: [
        {},
        {}
      ],
      family_members: [
        {}
      ],
      children_work_experiences: [
        {}
      ]
    }
  },
  created() {
    $.get('?get_selector_choices', (data) => {
      this.choices = data;

      this.educations = Object.keys(this.choices.education_types).map(t => {
        return {
          education_type: t,
          year_of_admission: '',
          year_of_graduation: '',
          degree: ''
        };
      });
    });
  },
  methods: {
    getInstitutionName(educationType) {
      return this.choices.education_types[educationType];
    },

    addEducationObject() {
      this.educations.push({
        education_type: '',
        year_of_admission: '',
        year_of_graduation: '',
        degree: ''
      })

      this.errors.educations.push({});
    },
    addJobObject() {
      this.jobs.push({
        is_current: false,
        organization_name: '',
        date_since: '',
        date_till: '',
        contact_info: '',
        position: '',
        duties: '',
        reason_for_leaving: ''
      })

      this.errors.jobs.push({});
    },
    addFamilyMemberObject() {
      this.family_members.push({
        name: '',
        gender: '',
        date_of_birth: '',
        relation: ''
      })

      this.errors.family_members.push({});
    },
    addChildrenWorkExperienceObject() {
      this.children_work_experiences.push({
        organization_name: '',
        date_since: '',
        date_till: '',
        contact_info: '',
        position: '',
        duties: '',
        children_age_group: ''
      })

      this.errors.children_work_experiences.push({});
    },
    submitForm() {
      const thisData = this;

      const data = Object.assign({}, this.$data);
      delete data.choices;
      delete data.errors;

      $.ajax({
        url: '',
        data: JSON.stringify(data),
        contentType: 'application/json',
        type: 'POST',
        success: (res) => {
          if (res.status === 'success') {
            window.location.href = "/mentor/register-step3/";
          } else {
            thisData.errors = res;
          }
        }
      });
    }
  }
});