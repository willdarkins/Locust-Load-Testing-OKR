LINE_ITEM_ROWS_QUERY = """
query LineItemRows($filter: LineItemsFilterInput, $page: PageInput, $sort: [LineItemsSortInput!], $paceInput: PaceMetricsInput, $hasPaceInput: Boolean! = false) {
  lineItems(filter: $filter, page: $page, sort: $sort) {
    pageInfo {
      pageNumber
      pageSize
      totalPages
      totalCount
      __typename
    }
    results {
      ...LineItemRow
      __typename
    }
    __typename
  }
}

fragment LineItemRow on LineItem {
  advertiser {
    ...AdvertiserWithHierarchy
    __typename
  }
  assignee {
    ...User
    __typename
  }
  created
  dateOfOrder
  endDate
  externalCampaigns {
    ...ExternalCampaignWithPace
    __typename
  }
  paceMetrics(input: $paceInput) @include(if: $hasPaceInput) {
    ...LineItemPaceMetric
    __typename
  }
  externalId
  flags
  id
  messageConversationUpdated
  name
  notesConversation {
    ...ConversationWithMessages
    __typename
  }
  order {
    ...OrderOnLineItem
    __typename
  }
  productListing {
    ...AdvertiserProductListing
    __typename
  }
  retailBudget
  requester {
    ...User
    __typename
  }
  startDate
  status
  __typename
}

fragment AdvertiserWithHierarchy on Advertiser {
  hierarchy {
    ...HierarchyWithParent
    __typename
  }
  id
  industry
  name
  website
  __typename
}

fragment HierarchyWithParent on Hierarchy {
  ...Hierarchy
  parent {
    ...HierarchyWithPartnerMetadata
    __typename
  }
  __typename
}

fragment Hierarchy on Hierarchy {
  id
  name
  __typename
}

fragment HierarchyWithPartnerMetadata on Hierarchy {
  id
  name
  partnerMetadata {
    ...PartnerMetadata
    __typename
  }
  __typename
}

fragment PartnerMetadata on PartnerMetadata {
  exportFileTypes
  exportTemplates
  accentColor
  primaryColor
  primaryPartnerSubsidiary {
    ...PartnerSubsidiary
    __typename
  }
  __typename
}

fragment PartnerSubsidiary on PartnerSubsidiary {
  id
  primary
  subsidiary {
    ...Subsidiary
    __typename
  }
  __typename
}

fragment Subsidiary on Subsidiary {
  countryCode
  currencyCode
  default
  id
  name
  __typename
}

fragment User on User {
  id
  fullName
  email
  __typename
}

fragment ExternalCampaignWithPace on ExternalCampaign {
  name
  id
  platformAdvertiserId
  platformCampaignId
  platform
  adGroupPaceMetrics(input: $paceInput) @include(if: $hasPaceInput) {
    ...AdGroupPaceMetric
    __typename
  }
  paceMetrics(input: $paceInput) @include(if: $hasPaceInput) {
    ...CampaignPaceMetric
    __typename
  }
  lineItem {
    ...LineItemOption
    __typename
  }
  __typename
}

fragment AdGroupPaceMetric on AdGroupPaceMetric {
  platform
  platformAdGroupId
  platformCampaignId
  clicks
  cpc {
    ...Currency
    __typename
  }
  cpv {
    ...Currency
    __typename
  }
  ctr
  impressions
  totalSpend {
    ...Currency
    __typename
  }
  views
  viewRate
  externalAdGroup {
    ...ExternalAdGroup
    __typename
  }
  __typename
}

fragment Currency on Currency {
  currencyUnit
  amount
  __typename
}

fragment ExternalAdGroup on ExternalAdGroup {
  id
  name
  platform
  platformAdGroupId
  platformAdvertiserId
  platformCampaignId
  __typename
}

fragment CampaignPaceMetric on CampaignPaceMetric {
  clicks
  cpc {
    ...Currency
    __typename
  }
  cpv {
    ...Currency
    __typename
  }
  ctr
  impressions
  totalSpend {
    ...Currency
    __typename
  }
  views
  viewRate
  __typename
}

fragment LineItemOption on LineItem {
  id
  name
  __typename
}

fragment LineItemPaceMetric on LineItemPaceMetric {
  lineItemId
  cpv {
    ...Currency
    __typename
  }
  ctr
  dailyBudget {
    ...Currency
    __typename
  }
  dailyImpressionsCap
  daysLeft
  goalDailyBudget {
    ...Currency
    __typename
  }
  impressionPace
  impressions
  orderedAdSpend {
    ...Currency
    __typename
  }
  orderedClicks
  orderedImpressions
  orderedViews
  projectedSpend {
    ...Currency
    __typename
  }
  projectedSpendDelta {
    ...Currency
    __typename
  }
  spendPace
  totalSpend {
    ...Currency
    __typename
  }
  viewPace
  viewRate
  views
  averageDailySpend {
    ...Currency
    __typename
  }
  clickPace
  clicks
  cpc {
    ...Currency
    __typename
  }
  __typename
}

fragment ConversationWithMessages on ConversationType {
  id
  messages {
    results {
      ...MessageOption
      __typename
    }
    __typename
  }
  __typename
}

fragment MessageOption on MessageType {
  body
  bodyPlainText
  id
  __typename
}

fragment OrderOnLineItem on Order {
  id
  name
  state
  __typename
}

fragment AdvertiserProductListing on AdvertiserProductListing {
  advertiserId
  goalTypes
  name
  product {
    ...Product
    __typename
  }
  productId
  __typename
}

fragment Product on ProductResponse {
  id
  description
  legacyProductKeys
  name
  productForms {
    ...ProductForm
    __typename
  }
  type
  ... on AdvertisingProduct {
    advertisingClass
    advertisingLine
    advertisingType
    platforms
    platformTargetingTypes {
      ...PlatformTargetingType
      __typename
    }
    managedByHierarchy {
      ...Hierarchy
      __typename
    }
    __typename
  }
  __typename
}

fragment ProductForm on ProductForm {
  appId
  id
  name
  type
  __typename
}

fragment PlatformTargetingType on PlatformTargetingType {
  platform
  type
  __typename
}
"""

# Default variables for line items query
LINE_ITEM_ROWS_VARIABLES = {
    "hasPaceInput": False,
    "filter": {
        "state": "MANAGED",
        "dates": {},
        "query": "",
        "statuses": [
            "CANCELED",
            "COMPLETE",
            "LIVE",
            "NEW",
            "PAUSED",
            "PENDING",
            "SOLD"
        ]
    },
    "page": {
        "pageSize": 25
    },
    "paceInput": None,
    "sort": {
        "direction": "DESC",
        "field": "DATE_OF_ORDER"
    }
}