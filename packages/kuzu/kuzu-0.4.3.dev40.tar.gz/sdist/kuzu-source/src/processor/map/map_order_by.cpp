#include "planner/operator/logical_order_by.h"
#include "processor/operator/order_by/order_by.h"
#include "processor/operator/order_by/order_by_merge.h"
#include "processor/operator/order_by/order_by_scan.h"
#include "processor/operator/order_by/top_k.h"
#include "processor/operator/order_by/top_k_scanner.h"
#include "processor/plan_mapper.h"

using namespace kuzu::common;
using namespace kuzu::planner;

namespace kuzu {
namespace processor {

std::unique_ptr<PhysicalOperator> PlanMapper::mapOrderBy(LogicalOperator* logicalOperator) {
    auto& logicalOrderBy = logicalOperator->constCast<LogicalOrderBy>();
    auto outSchema = logicalOrderBy.getSchema();
    auto inSchema = logicalOrderBy.getChild(0)->getSchema();
    auto prevOperator = mapOperator(logicalOrderBy.getChild(0).get());
    auto keyExpressions = logicalOrderBy.getExpressionsToOrderBy();
    auto payloadExpressions = inSchema->getExpressionsInScope();
    std::vector<DataPos> payloadsPos;
    std::vector<LogicalType> payloadTypes;
    binder::expression_map<ft_col_idx_t> payloadToColIdx;
    auto payloadSchema = FactorizedTableSchema();
    auto mayContainUnFlatKey = inSchema->getNumGroups() == 1;
    for (auto i = 0u; i < payloadExpressions.size(); ++i) {
        auto expression = payloadExpressions[i];
        auto [dataChunkPos, vectorPos] = inSchema->getExpressionPos(*expression);
        payloadsPos.emplace_back(dataChunkPos, vectorPos);
        payloadTypes.push_back(expression->dataType.copy());
        if (!inSchema->getGroup(dataChunkPos)->isFlat() && !mayContainUnFlatKey) {
            // payload is unFlat and not in the same group as keys
            auto columnSchema =
                ColumnSchema(true /* isUnFlat */, dataChunkPos, sizeof(overflow_value_t));
            payloadSchema.appendColumn(std::move(columnSchema));
        } else {
            auto columnSchema = ColumnSchema(false /* isUnFlat */, dataChunkPos,
                LogicalTypeUtils::getRowLayoutSize(expression->getDataType()));
            payloadSchema.appendColumn(std::move(columnSchema));
        }
        payloadToColIdx.insert({expression, i});
    }
    std::vector<DataPos> keysPos;
    std::vector<LogicalType> keyTypes;
    std::vector<uint32_t> keyInPayloadPos;
    for (auto& expression : keyExpressions) {
        keysPos.emplace_back(inSchema->getExpressionPos(*expression));
        keyTypes.push_back(expression->getDataType().copy());
        KU_ASSERT(payloadToColIdx.contains(expression));
        keyInPayloadPos.push_back(payloadToColIdx.at(expression));
    }
    std::vector<DataPos> outPos;
    for (auto& expression : payloadExpressions) {
        outPos.emplace_back(outSchema->getExpressionPos(*expression));
    }
    auto orderByDataInfo = std::make_unique<OrderByDataInfo>(keysPos, payloadsPos,
        LogicalType::copy(keyTypes), LogicalType::copy(payloadTypes),
        logicalOrderBy.getIsAscOrders(), std::move(payloadSchema), std::move(keyInPayloadPos));
    auto printInfo = std::make_unique<OPPrintInfo>(logicalOrderBy.getExpressionsForPrinting());
    if (logicalOrderBy.isTopK()) {
        auto topKSharedState = std::make_shared<TopKSharedState>();
        auto topK = make_unique<TopK>(std::make_unique<ResultSetDescriptor>(inSchema),
            std::move(orderByDataInfo), topKSharedState, logicalOrderBy.getSkipNum(),
            logicalOrderBy.getLimitNum(), std::move(prevOperator), getOperatorID(),
            printInfo->copy());
        return make_unique<TopKScan>(outPos, topKSharedState, std::move(topK), getOperatorID(),
            printInfo->copy());
    } else {
        auto orderBySharedState = std::make_shared<SortSharedState>();
        auto orderBy = make_unique<OrderBy>(std::make_unique<ResultSetDescriptor>(inSchema),
            std::move(orderByDataInfo), orderBySharedState, std::move(prevOperator),
            getOperatorID(), printInfo->copy());
        auto dispatcher = std::make_shared<KeyBlockMergeTaskDispatcher>();
        auto orderByMerge = make_unique<OrderByMerge>(orderBySharedState, std::move(dispatcher),
            std::move(orderBy), getOperatorID(), printInfo->copy());
        return make_unique<OrderByScan>(outPos, orderBySharedState, std::move(orderByMerge),
            getOperatorID(), printInfo->copy());
    }
}

} // namespace processor
} // namespace kuzu
