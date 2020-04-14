{% block header %}{% endblock %}
{% set module_name = 'xsd_types_module' %}
{% set domain = 'Unknown' %}
{% set taglen = 100 %}
!
MODULE {{ module_name }}
  !
  ! Auto-generated code: don't edit this file
  !
  ! {{ domain }} XSD namespace: {{schema.target_namespace}}
  !
  {%  block module_settings %}{% endblock %}
  !a
{%- for xsd_type in schema.iter_complex_types() %}
  TYPE :: {{ xsd_type | fortran_type }}
    !
    CHARACTER(len=100) :: tagname
    LOGICAL  :: lwrite = .FALSE.
    LOGICAL  :: lread  = .FALSE.
    !
  {%- for xsd_attribute in xsd_type.attributes.values() %}
    {{ xsd_attribute.type | fortran_type }} :: {{ xsd_attribute.name}}
    {%- if not xsd_attribute.is_required() %}
    LOGICAL :: {{ xsd_attribute.name }}_ispresent = .FALSE.
    {%- endif %}
  {%- endfor %}

  {%- if xsd_type.is_extension() %}
    {%- if xsd_type.base_type is not None %}
      {%- for xsd_attribute in xsd_type.base_type.attributes.values() %}
    {{xsd_attribute.type | fortran_type }} :: {{ xsd_attribute.name }}
        {%- if not xsd_attribute.is_required() %}
    LOGICAL :: {{xsd_attribute.name}}_ispresent = .FALSE.
        {%- endif %}
      {%- endfor %}
    {%- endif %}
    !
    {{ xsd_type.base_type | fortran_type }} :: {{ xsd_type.name.replace('Type', '') }}
  {%- endif %}
    !
  {%- for xsd_element in xsd_type.iter_elements() %}
    {%- if not xsd_element.min_occurs %}
    LOGICAL  :: {{ xsd_element.local_name}}_ispresent = .FALSE.
    {%- endif %}
    {%- if xsd_element.max_occurs == 1 %}
      {%- if (element.is_qes_type) and (not element.xsd_type.is_simple() )%}
    TYPE({{element.fortran_type_name()}}) :: {{element.tag_name}}
      {%- else %}
    {{ element.fortran_type_name() }} :: {{element.tag_name}}
      {%- endif %}
{%- else %}
    TYPE({{element.xsd_type.fortran_type_name()}}), DIMENSION(:), ALLOCATABLE :: {{element.tag_name}}
    INTEGER   :: ndim_{{element.tag_name}}
{%- endif %}
{%- endfor %}
    !
  END TYPE {{ xsd_type | fortran_type }}
  !
{%- endfor %}
  !
END MODULE {{ module_name }}
